from django import forms
from .models import Comment, BlogPost


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'overview', 'thumbnail']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Post Title', 'required': ''}),
            'overview': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write here...', 'required': ''}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your comment here...', 'required': ''}),
        }