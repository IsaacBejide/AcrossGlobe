from django import forms
from django.urls import reverse_lazy
from .models import *  #Profile, BlogPost, BlogPostCategories, FileUploads, Comment, ReplyComment, CommentFileUploads, Advertisement
from ckeditor.widgets import CKEditorWidget
from django.forms import ClearableFileInput
from ckeditor.fields import RichTextFormField
from django.utils.translation import gettext_lazy as _
# from ckeditor.widgets import RichTextFormField
from django.contrib.auth.forms import UserCreationForm as UserCreationFormBase
from bootstrap_modal_forms.forms import BSModalModelForm
from datetime import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


CATEGORY_TYPES = [
    ('1', 'General'),
    ('2', 'Entertainment'),
    ('3', 'Science/Technology'),
]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = BlogPostCategories
        fields = ('type', 'category_title',)
        widgets = {
            #     'type':forms.Select(TypeCategories),
            'category_title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blog Category'}),
        }


class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='Message:')

    class Meta:
        model = BlogPost
        # fields='__all__'
        fields = ('title', 'content',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title of the Blog'}),
        }


class FileUploadForm(forms.ModelForm):
    # file = ClearableFileInput(label='Message:')
    class Meta:
        model = FileUploads
        fields = ('file',)
        widgets = {
            'file': ClearableFileInput(
                attrs={'multiple': True, 'placeholder': 'Select multiple files, maximum of 4 files'}),
        }


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), label='Message:')

    class Meta:
        model = Comment
        fields = ('content',)
        # widgets = {
        #     'content': RichTextFormField(config_name='default'), 
        #     #'content': RichTextFormField(config_name='default'), 
        # }
        

class Reply_CommentForm(forms.ModelForm):
    reply_content = forms.CharField(widget=CKEditorWidget(), label='Message:')
    class Meta:
        model = ReplyComment
        fields = ('reply_content',)
        # widgets = {
        #     'content': RichTextFormField(config_name='default'), 
        #     #'content': RichTextFormField(config_name='default'), 
        # }


class CommentFileUploadForm(forms.ModelForm):
    class Meta:
        model = CommentFileUploads
        fields = ('file',)
        widgets = {
            'file': ClearableFileInput(
                attrs={'multiple': True, 'placeholder': 'Select multiple files, maximum of 4 files'}),
        }


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    recepient_email = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)


#  Lazy Users

class UserCreationForm(UserCreationFormBase):

    def get_credentials(self):
        return {
            'username': self.cleaned_data['username'],
            'password': self.cleaned_data['password1']}


class AdvertisementForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_action = reverse_lazy('advertisement')
    #     self.helper.form_method = 'GET'
    #     self.helper.add_input(Submit('submit', 'Submit'))
    
    
    expiration_date = forms.DateField(label='Start Date:', widget=forms.DateInput(attrs={'type': 'date', 'min': datetime.now().date()}))
    #expiration_date = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'], widget=forms.DateTimeInput(attrs={'class': 'form-control datetimepicker-input', 'data-target': '#datetimepicker1'}))
    class Meta:
        model = Advertisement
        fields = ('urllink', 'advertiser', 'image', )
        labels = {
            'urllink': 'Landing Page',
            'advertiser': 'Advert Owner Name'
        }
       