from django import forms
from posts.models import Post


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body',)