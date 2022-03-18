from django.forms import ModelForm
from django import forms
from .models import Post


class PostCreationForm(ModelForm):
    name = forms.CharField(max_length=30, required=False, help_text="Your nickname[optional]")
    class Meta:
        model = Post
        fields = ['name', 'image', 'title', 'body']