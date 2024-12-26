from django.contrib import admin
from django.contrib.auth import admin as auth_admin

from app.accounts.forms import UserChangeForm, UserCreationForm
from app.accounts.models import Users


@admin.register(Users)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        ("Campos personalizados", {"fields": ("bio",)}),
    )
