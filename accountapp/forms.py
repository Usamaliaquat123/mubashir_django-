from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import Group
from accountapp.models import *
from jobapp.models import *
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import forms as auth_forms
from django.forms import ModelForm
from django.contrib.auth.password_validation import validate_password
from django.forms.models import inlineformset_factory

#login form
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={'placeholder': 'Email Address'}),label='Email Address')
    password = forms.CharField(widget=PasswordInput(attrs={'placeholder':'Password'}))
    
    def __init__(self, *args, **kwargs):
            super(LoginForm, self).__init__(*args, **kwargs)

            self.fields['username'].label = 'Email Address'
            self.fields['password'].label = 'Password'

            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

    def clean(self, *args, **kwargs):
         username = self.cleaned_data.get("username")
         password = self.cleaned_data.get("password")
         if username and password:
            info = User.objects.filter(email = username, groups__name='Employer').first()
            if not info:
               raise ValidationError("This email address does not exists")
            user = authenticate(email=info.email, password=password)
            if not user:
                if info.is_active: 
                    raise ValidationError("Invalid password")
                else:
                    raise ValidationError("This account is inactive.")
            return True

#Profile form
class ProfileForm(forms.ModelForm):

    company         = forms.CharField(max_length=55, required=True, label='Company', widget=forms.TextInput(attrs={'placeholder': 'Enter your Company'}))
    title           = forms.CharField(max_length=30, required=False, label='Title', widget=forms.TextInput(attrs={'placeholder': 'Enter your Title'}))
    first_name      = forms.CharField(max_length=30, required=True, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'Enter your First Name'}))
    last_name       = forms.CharField(max_length=30, required=True, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Enter your Last Name'}))
    
    class Meta:
        model = User
        fields = ['image','first_name','last_name','company','title','email','mobile']
    
    def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            self.fields['mobile'].required                          = True
            self.fields['mobile'].widget.attrs['placeholder']       = 'Enter your Phone #'
            self.fields['email'].widget.attrs['placeholder']        = 'Enter your Email Address'
            self.fields['email'].label                              = 'Email Address'
            self.fields['mobile'].label                             = 'Phone'
            self.fields['image'].label                              = 'Take Picture / Upload File'
            
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        alreadyexist = User.objects.filter(email=email).first()
        if alreadyexist:
            if alreadyexist.id != self.instance.id:
                raise ValidationError('User with this email address already exists.')
        return email

#employer create form
class RegisterForm(ModelForm):

    company         = forms.CharField(max_length=55, required=True, label='Company', widget=forms.TextInput(attrs={'placeholder': 'Enter your Company'}))
    title           = forms.CharField(max_length=30, required=False, label='Title', widget=forms.TextInput(attrs={'placeholder': 'Enter your Title'}))
    first_name      = forms.CharField(max_length=30, required=True, label='First Name', widget=forms.TextInput(attrs={'placeholder': 'Enter your First Name'}))
    last_name       = forms.CharField(max_length=30, required=True, label='Last Name', widget=forms.TextInput(attrs={'placeholder': 'Enter your Last Name'}))
    password1       = forms.CharField(max_length=30, required=True, label='Create your Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Password'}))
    password2       = forms.CharField(max_length=30, required=True, label='Confirm Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter your Confirm Password'}))
    
    class Meta:
        model = User
        fields = ['image','first_name','last_name','company','title','email','mobile','password1','password2']
    
    def __init__(self, *args, **kwargs):
            super(RegisterForm, self).__init__(*args, **kwargs)
            self.fields['mobile'].required                          = True
            self.fields['mobile'].widget.attrs['placeholder']       = 'Enter your Phone #'
            self.fields['email'].widget.attrs['placeholder']        = 'Enter your Email Address'
            self.fields['email'].label                              = 'Email Address'
            self.fields['mobile'].label                             = 'Phone'
            self.fields['image'].label                              = 'Take Picture / Upload File'
            
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        email           = self.cleaned_data['email'].lower()
        alreadyexist    = User.objects.filter(email=email).first()
        if alreadyexist:
            if alreadyexist.id != self.instance.id:
                raise ValidationError('User with this email address already exists.')
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        validate_password(password2,self.instance)
        return password2

#Password Reset Request Form
class PasswordResetRequestForm(forms.Form):

    email   =  forms.EmailField(label=("Email Address"), max_length=254)
    
    def __init__(self, *args, **kwargs):
            super(PasswordResetRequestForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    
    def clean(self, *args, **kwargs):
         email  = self.cleaned_data.get("email")
         if email:
            email = email.lower()
            info = User.objects.filter(email=email).first()
            if not info:
               raise ValidationError("This email address does not exists")
            return True

#Job List Filter
class JobSeekerFilter(forms.Form):
<<<<<<< HEAD
    search      = forms.CharField(required=False, label='Location',widget=TextInput(attrs={'placeholder': 'City, State or Zip'}),)
    radius      = forms.CharField(required=False, label='Radius',widget=TextInput(attrs={'placeholder': 'Miles','type':'number'}),)
=======
    search      = forms.CharField(required=False, label='Search By',widget=TextInput(attrs={'placeholder': 'Search by city, state & zipcode'}),)
    radius      = forms.CharField(required=False, label='Radius (miles)',widget=TextInput(attrs={'placeholder': 'Search by Radius(miles)','type':'number'}),)
>>>>>>> alt-history
    category    = forms.ModelMultipleChoiceField(label='Category', required=False,queryset=Category.objects.filter(publish=True).order_by('name'),widget=forms.CheckboxSelectMultiple)


#employer create form
class ContactUsForm(ModelForm):

    class Meta:
        model  = ContactUs
        fields = ['name','email','phone','message']
    
    def __init__(self, *args, **kwargs):
            super(ContactUsForm, self).__init__(*args, **kwargs)
            self.fields['message'].required             = True
            self.fields['message'].widget.attrs['rows'] = 3
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#employer create form
class SubscriptionForm(ModelForm):

    class Meta:
        model  = Subscription
        fields = ['user','plan',]
    
    def __init__(self, *args, **kwargs):
            user  = kwargs.pop('user', None)
            plan  = kwargs.pop('plan', None)
            super(SubscriptionForm, self).__init__(*args, **kwargs)
            self.fields['user'].initial              = user
            self.fields['user'].widget               = forms.HiddenInput()
            self.fields['plan'].initial              = plan
            self.fields['plan'].widget               = forms.HiddenInput()
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
