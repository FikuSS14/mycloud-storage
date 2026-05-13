from django.contrib import admin
from django.urls import path
from core.views import (
    RegisterView, LoginView, LogoutView, MeView,
    UserListView, UserPromoteView, 
    FileListView, FileUploadView, FileDeleteView,
    FileRenameView, FileCommentView, FileDownloadView, FileDownloadByLinkView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/me/', MeView.as_view(), name='me'),
    
    # Админские API
    path('api/users/', UserListView.as_view(), name='user-list'),
    path('api/users/<int:user_id>/', UserListView.as_view(), name='user-delete'),
    path('api/users/<int:user_id>/promote/', UserPromoteView.as_view(), name='user-promote'),
    
    # API для работы с файлами
    path('api/files/', FileListView.as_view(), name='file-list'),
    path('api/files/upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/files/<int:file_id>/', FileDeleteView.as_view(), name='file-delete'),
    path('api/files/<int:file_id>/rename/', FileRenameView.as_view(), name='file-rename'),
    path('api/files/<int:file_id>/comment/', FileCommentView.as_view(), name='file-comment'),
    path('api/files/<int:file_id>/download/', FileDownloadView.as_view(), name='file-download'),
    
    # Публичная ссылка (не требует авторизации)
    path('api/download/<str:special_link>/', FileDownloadByLinkView.as_view(), name='download-by-link'),
]