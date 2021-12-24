from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import Group
from blogapp.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_forms
from django.forms import ModelForm
from django.contrib.auth.password_validation import validate_password
from django.forms.models import inlineformset_factory

#Blog List Filter
class BlogListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Title'}),)
    category    = forms.CharField(widget = forms.HiddenInput(), required = False)


