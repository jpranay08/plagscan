from django import forms
from .models import Post


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content','document']
