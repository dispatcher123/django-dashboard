from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets=()
    list_filter=('is_admin','is_active')
    list_display=('id','email','username','login_date','is_active','is_admin')
    filter_horizontal=()
    
