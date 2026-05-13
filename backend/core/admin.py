from django.contrib import admin
from .models import User, File

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'login', 'full_name', 'email', 'is_admin')
    search_fields = ('login', 'email')

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'original_name', 'user', 'size', 'upload_date')
    search_fields = ('original_name', 'user__login')