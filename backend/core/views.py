import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rest_framework.parsers import MultiPartParser, FormParser
from .models import File as FileModel
from .serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .models import User
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


# Регистрация (доступно всем)
class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'Пользователь успешно зарегистрирован',
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Логин (доступно всем)
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        # Просто отдаём пустой ответ, чтобы Django создал CSRF-токен
        return Response({'message': 'CSRF token set'}, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            login_input = serializer.validated_data['login']
            password = serializer.validated_data['password']
            user = authenticate(request, username=login_input, password=password)
            if user is not None:
                login(request, user)
                return Response({
                    'message': 'Вход выполнен успешно',
                    'user': UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Логаут (только для авторизованных)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Выход выполнен успешно'}, status=status.HTTP_200_OK)

# Проверка текущего пользователя (кто я?)
class MeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(UserSerializer(request.user).data)
    
# Список пользователей и управление ими (только админ)
class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Проверяем, что текущий пользователь - админ
        if not request.user.is_admin:
            return Response({'error': 'Доступ запрещён. Требуются права администратора.'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def delete(self, request, user_id):
        # Проверяем, что текущий пользователь - админ
        if not request.user.is_admin:
            return Response({'error': 'Доступ запрещён. Требуются права администратора.'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
            # Не даём админу удалить самого себя (чтобы не сломать систему)
            if user.id == request.user.id:
                return Response({'error': 'Нельзя удалить самого себя'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            user.delete()
            return Response({'message': 'Пользователь удалён'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

# Изменение прав пользователя (назначение/снятие админа)
class UserPromoteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        # Проверяем, что текущий пользователь - админ
        if not request.user.is_admin:
            return Response({'error': 'Доступ запрещён. Требуются права администратора.'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
            # Переключаем флаг is_admin
            user.is_admin = not user.is_admin
            user.save()
            return Response({
                'message': f'Права администратора {"назначены" if user.is_admin else "сняты"}',
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        
# Получение списка файлов (для текущего пользователя или для админа - любого)
class FileListView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        print(f"DEBUG: User = {request.user.login}, is_admin = {request.user.is_admin}")
        
        # Если админ и передан параметр user_id - показываем файлы другого пользователя
        user_id = request.query_params.get('user_id')
        if user_id and request.user.is_admin:
            try:
                target_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            target_user = request.user
        
        files = FileModel.objects.filter(user=target_user)
        print(f"DEBUG: Found {files.count()} files for user {target_user.login}")
        
        serializer = FileSerializer(files, many=True)
        return Response(serializer.data)

# Загрузка файла
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def post(self, request):
        # Определяем, кому загружаем файл (админ может загружать другому пользователю)
        user_id = request.data.get('user_id')
        if user_id and request.user.is_admin:
            try:
                target_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        else:
            target_user = request.user
        
        uploaded_file = request.FILES.get('file')
        comment = request.data.get('comment', '')
        
        if not uploaded_file:
            return Response({'error': 'Файл не передан'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Генерируем уникальное имя файла на диске
        import uuid
        unique_filename = f"{uuid.uuid4().hex}_{uploaded_file.name}"
        
        # Создаём папку пользователя, если её нет
        user_folder = os.path.join(settings.MEDIA_ROOT, f"user_{target_user.login}")
        os.makedirs(user_folder, exist_ok=True)
        
        # Сохраняем файл
        file_path = os.path.join(user_folder, unique_filename)
        saved_path = default_storage.save(file_path, ContentFile(uploaded_file.read()))
        
        # Создаём запись в БД
        file_obj = FileModel(
            user=target_user,
            original_name=uploaded_file.name,
            comment=comment,
            size=uploaded_file.size,
            file_path=saved_path,
            special_link=FileModel.generate_special_link(None)  # временно, потом переделаем
        )
        file_obj.special_link = file_obj.generate_special_link()
        file_obj.save()
        
        serializer = FileSerializer(file_obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Удаление файла
class FileDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, file_id):
        try:
            file_obj = FileModel.objects.get(id=file_id)
        except FileModel.DoesNotExist:
            return Response({'error': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        # Проверяем права: владелец или админ
        if file_obj.user != request.user and not request.user.is_admin:
            return Response({'error': 'Нет прав на удаление этого файла'}, status=status.HTTP_403_FORBIDDEN)
        
        # Удаляем физический файл
        if os.path.exists(file_obj.file_path):
            os.remove(file_obj.file_path)
        
        # Удаляем запись из БД
        file_obj.delete()
        
        return Response({'message': 'Файл удалён'}, status=status.HTTP_200_OK)
    
    # Переименование файла
class FileRenameView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, file_id):
        try:
            file_obj = FileModel.objects.get(id=file_id)
        except FileModel.DoesNotExist:
            return Response({'error': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        # Проверка прав
        if file_obj.user != request.user and not request.user.is_admin:
            return Response({'error': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)
        
        new_name = request.data.get('original_name')
        if not new_name:
            return Response({'error': 'Не указано новое имя'}, status=status.HTTP_400_BAD_REQUEST)
        
        file_obj.original_name = new_name
        file_obj.save()
        
        return Response(FileSerializer(file_obj).data)

# Изменение комментария
class FileCommentView(APIView):
    permission_classes = [IsAuthenticated]
    
    def patch(self, request, file_id):
        try:
            file_obj = FileModel.objects.get(id=file_id)
        except FileModel.DoesNotExist:
            return Response({'error': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        if file_obj.user != request.user and not request.user.is_admin:
            return Response({'error': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)
        
        comment = request.data.get('comment', '')
        file_obj.comment = comment
        file_obj.save()
        
        return Response(FileSerializer(file_obj).data)

# Скачивание файла по специальной ссылке (обезличенной)
class FileDownloadByLinkView(APIView):
    permission_classes = [AllowAny]  # Доступно всем по ссылке
    
    def get(self, request, special_link):
        try:
            file_obj = FileModel.objects.get(special_link=special_link)
        except FileModel.DoesNotExist:
            return Response({'error': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        from django.http import FileResponse
        import os
        
        # Обновляем дату последнего скачивания
        from django.utils import timezone
        file_obj.last_download_date = timezone.now()
        file_obj.save()
        
        # Отдаём файл
        response = FileResponse(open(file_obj.file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.original_name}"'
        return response

# Скачивание файла для авторизованного пользователя
class FileDownloadView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, file_id):
        try:
            file_obj = FileModel.objects.get(id=file_id)
        except FileModel.DoesNotExist:
            return Response({'error': 'Файл не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        if file_obj.user != request.user and not request.user.is_admin:
            return Response({'error': 'Нет прав'}, status=status.HTTP_403_FORBIDDEN)
        
        from django.http import FileResponse
        from django.utils import timezone
        
        file_obj.last_download_date = timezone.now()
        file_obj.save()
        
        response = FileResponse(open(file_obj.file_path, 'rb'), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.original_name}"'
        return response