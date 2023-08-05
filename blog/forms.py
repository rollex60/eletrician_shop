from django import forms
from django.contrib.auth import get_user_model
from django.forms import Textarea

from blog.models import Comment

User = get_user_model()


class CommentsForm(forms.ModelForm):
    # ----Comment Form------------------------------------------------------------------------------
    
    class Meta:
        model = Comment
        fields = ('text',)
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget = Textarea(attrs={'rows':5})