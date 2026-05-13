from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
import os

class UserManager(BaseUserManager):
    def create_user(self, login, full_name, email, password=None, is_admin=False):
        if not login:
            raise ValueError('Login обязателен')
        if not email:
            raise ValueError('Email обязателен')
        user = self.model(
            login=login,
            full_name=full_name,
            email=self.normalize_email(email),
            is_admin=is_admin,
            storage_path=f'user_{login}' 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, login, full_name, email, password=None):
        user = self.create_user(login, full_name, email, password, is_admin=True)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    login = models.CharField(max_length=20, unique=True, verbose_name='Логин')
    full_name = models.CharField(max_length=255, verbose_name='Полное имя')
    email = models.EmailField(unique=True, verbose_name='Email')
    is_admin = models.BooleanField(default=False, verbose_name='Администратор')
    storage_path = models.CharField(max_length=255, verbose_name='Путь к хранилищу')
    
    USERNAME_FIELD = 'login'  
    REQUIRED_FIELDS = ['full_name', 'email']  
    
    objects = UserManager()
    
    def __str__(self):
        return self.login
    
    @property
    def is_staff(self):
        return self.is_admin
    
    @property
    def is_superuser(self):
        return self.is_admin
    
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return self.is_admin

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='files', verbose_name='Владелец')
    original_name = models.CharField(max_length=255, verbose_name='Оригинальное имя')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    size = models.BigIntegerField(verbose_name='Размер в байтах')
    upload_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    last_download_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата последнего скачивания')
    file_path = models.CharField(max_length=500, verbose_name='Путь к файлу на диске')
    special_link = models.CharField(max_length=255, unique=True, verbose_name='Специальная ссылка')
    
    def __str__(self):
        return f"{self.user.login}/{self.original_name}"
    
    def generate_special_link(self):
        """Генерирует обезличенную ссылку: UUID без логина и имени файла"""
        return str(uuid.uuid4()).replace('-', '')[:32]
    
    def save(self, *args, **kwargs):
        if not self.special_link:
            self.special_link = self.generate_special_link()
        super().save(*args, **kwargs)