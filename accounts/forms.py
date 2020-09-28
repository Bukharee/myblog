from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import CustomUser
from blog.models import PostPicture, Folder


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)


    class Meta:
        model = get_user_model()
        fields =  ['username', 'email',]


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError("password dont match")
        return password2

    def save(self,commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'photo', 'bio', 'github', 'facebook', 'twitter']

class CreateFolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name',]

class PhotoUploadForm(forms.ModelForm):
    class Meta:
        model = PostPicture
        fields = ['name', 'photo',]