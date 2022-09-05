from django import forms
from .models import Comment, Reply, Post, Subscribe
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib import admin
from django.contrib.auth.models import User
from tinymce import TinyMCE


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', ]


class ReplyForm(forms.ModelForm):
    class Meta:
        name = get_user_model()
        model = Reply
        fields = ['name', 'text']


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, **kwargs):
        return False


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        slug = str(Post.title).replace(' ', '-')
        publish = timezone.now()
        fields = ['title', 'body', 'category',
                  'tags', 'next_post', 'previous_post']


class SearchForm(forms.Form):
    query = forms.CharField(widget=forms.TextInput(attrs={}), label="")


class SubscribingForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ['email', ]
