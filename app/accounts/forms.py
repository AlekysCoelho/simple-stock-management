from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from app.accounts.models import Users


class UsersCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ("bio",)


class UsersChangeForm(UserChangeForm):
    class Meta:
        model = Users
        fields = ("bio",)
