from django import forms
from django.forms import fields
from .models import BlogPost, Comment, Contact

class PostForm(forms.ModelForm):
    class Meta:
        model =BlogPost
        fields=['title','body','image','category']


class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']

class ContactForm(forms.ModelForm):
    class Meta:
        model=Contact
        fields=['email','first_name','last_name','message','number']
