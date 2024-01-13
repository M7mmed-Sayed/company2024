# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import PostType, Post, Image, Project


class PostTypeForm(forms.ModelForm):
    class Meta:
        model = PostType
        fields = ['name', 'description']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['postType', 'postSubject', 'postContent']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
