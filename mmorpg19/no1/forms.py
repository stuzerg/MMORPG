from django import forms
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm

from .models import post, review
# from django_filters import ModelMultipleChoiceFilter

from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.forms import ModelForm


class ReviewForm(ModelForm):
    reviewbody = forms.CharField(label="Отклик", widget=forms.Textarea)
    class Meta:

        fields = ['reviewbody']
        model = review


class PostListForm(forms.Form):
   content = forms.CharField(widget=CKEditorWidget())
   class Meta:
       model = post
       fields = [ 'header', 'body', 'staff', 'user'
       ]

class PostviewForm(ModelForm):
  # content = forms.CharField(widget=CKEditorWidget())

   class Meta:
       model = post
       fields = [ 'header', 'body', 'staff', 'id'
       ]