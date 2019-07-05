from django import forms
from .models import Trip, Comment

class TripForm(forms.ModelForm):
    
    class Meta:
        model = Trip        
        fields = ['title', 'body', 'transportation', 'place', 'person', 'budget']
        widgets = {
            'budget': forms.Select(),
            'transportation' : forms.Select(),
            'place' : forms.Select()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contents']

