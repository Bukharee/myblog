from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm, UserCreationForm
from django.contrib.auth.models import User


CustomUser = get_user_model()

class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm
    fieldsets = (
        (None, {
            'classes': ('wide '),
            'fields' : ('first_name', 'last_name','username','email', 'password', 'photo', 'bio', 'github', 'facebook', 
            'twitter','is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', 'last_login', 'date_joined')}),
    )
    list_display = ['email', 'username', 'bio', 'photo']
    
admin.site.register(CustomUser, UserAdmin)

# (None, {'fields' : ('username', 'password')}), (_('Personal info'), {'fields':('first_name', 'last_name', 'email', 'name', 'contact')}),
#         (_('Permission'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
#         (_('Important dates'), {'fields:' ('last_login')})