from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput
from django.contrib.auth.models import Group
from accountapp.models import *
from jobapp.models import *
from blogapp.models import *
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
            info = User.objects.filter(email = username, groups__name='Admin').first()
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

    first_name          = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a First Name'}))
    last_name           = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Last Name'}))
    class Meta:
        model = User
        fields = ['first_name','last_name','email']

    def __init__(self, *args, **kwargs):
            super(ProfileForm, self).__init__(*args, **kwargs)
            self.fields['email'].widget.attrs['placeholder'] = 'Enter a Email Address'

            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    
    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        alreadyexist = User.objects.filter(email=email).first()
        if alreadyexist:
            if alreadyexist.id != self.instance.id:
                raise ValidationError('User with this email address already exists.')
        return email

#Change Password form
class ChangePasswordForm(forms.ModelForm):

    password1           = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password'}),label='Password')
    password2           = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a confirm Password'}),label='Confirm Password')
    class Meta:
        model = User
        fields = ['password1','password2']

    def __init__(self, *args, **kwargs):
            super(ChangePasswordForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    
    def clean(self, *args, **kwargs):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError("Passwords don't match.")
        return self.cleaned_data

#employer create form
class EmployerCreateForm(ModelForm):

    company         = forms.CharField(max_length=55, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Company'}))
    title           = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Title'}))
    first_name      = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a First Name'}))
    last_name       = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Last Name'}))
    password1       = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password'}),label='Password')
    password2       = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a confirm Password'}),label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['image','first_name','last_name','company','title','email','mobile','password1','password2']
    
    def __init__(self, *args, **kwargs):
            super(EmployerCreateForm, self).__init__(*args, **kwargs)
            self.fields['mobile'].required                          = True
            self.fields['mobile'].widget.attrs['placeholder']       = 'Enter a Phone #'
            self.fields['email'].widget.attrs['placeholder']        = 'Enter a Email Address'
            self.fields['mobile'].label                             = 'Phone #'
            self.fields['image'].label                              = 'Current Image'
            
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        validate_password(password2,self.instance)
        return password2

#employer update form
class EmployerUpdateForm(ModelForm):
    company         = forms.CharField(max_length=55, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Company'}))
    title           = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Title'}))
    first_name     = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a First Name'}))
    last_name      = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Last Name'}))

    class Meta:
        model = User
        fields = ['image','first_name','last_name','company','title','email','mobile']


    def __init__(self, *args, **kwargs):
            super(EmployerUpdateForm, self).__init__(*args, **kwargs)

            self.fields['mobile'].label = ''
            self.fields['mobile'].required = True
            self.fields['mobile'].widget.attrs['placeholder']         = 'Enter a Phone #'
            self.fields['email'].widget.attrs['placeholder']         = 'Enter a Email Address'
            self.fields['image'].label = 'Take Picture / Upload File'

            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#Employer List Filter
class EmployerListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Company/Email/Name or Phone'}),)
    is_active   = forms.ChoiceField(required=False, label='Actived',choices=[('', '--- Select Activated --')] + [(False,'No'),(True,'Yes'),])

#jobseeker create form
class JobseekerCreateForm(ModelForm):

    first_name      = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a First Name'}))
    last_name       = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Last Name'}))
    state           = forms.ModelChoiceField(widget=forms.Select(attrs={'class': ''}),queryset = State.objects.filter(publish=True).order_by('name') , empty_label='Select State')
    city            = forms.ModelChoiceField(widget=forms.Select(attrs={'class': ''}),queryset = City.objects.filter(publish=True).order_by('name') , empty_label='Select City')
    password1       = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password'}),label='Password')
    password2       = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a confirm Password'}),label='Confirm Password')
    
    class Meta:
        model = User
        fields = ['image','video','first_name','last_name','state','city','address','zipcode','mobile','email','password1','password2','yourself','bg_check','available','IsProComplete','IsProCompleteStatus']
    
    def __init__(self, *args, **kwargs):
            super(JobseekerCreateForm, self).__init__(*args, **kwargs)
            self.fields['mobile'].required                          = True
            self.fields['address'].required                         = True
            self.fields['zipcode'].required                         = True
            self.fields['mobile'].widget.attrs['placeholder']       = 'Enter a Phone #'
            self.fields['email'].widget.attrs['placeholder']        = 'Enter a Email Address'
            self.fields['mobile'].label                             = 'Phone #'
            self.fields['image'].label                              = 'Upload Profile Picture'
            self.fields['video'].label                              = 'Upload Video Resume'
            self.fields['yourself'].label                           = 'Tell employers a little about yourself'
            self.fields['bg_check'].label                           = 'Are you willing to do a background check'
            self.fields['available'].label                          = 'Mark yourself available so employers can hire you'
            self.fields['IsProComplete'].label                      = 'Is Profile Complete'
            self.fields['IsProCompleteStatus'].label                = 'Is Profile Complete Status'

            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
    
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")
        validate_password(password2,self.instance)
        return password2

#jobseeker update form
class JobseekerUpdateForm(ModelForm):
    
    first_name      = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a First Name'}))
    last_name       = forms.CharField(max_length=30, required=True ,widget=forms.TextInput(attrs={'placeholder': 'Enter a Last Name'}))
    state           = forms.ModelChoiceField(widget=forms.Select(attrs={'class': ''}),queryset = State.objects.filter(publish=True).order_by('name') , empty_label='Select State')
    city            = forms.ModelChoiceField(widget=forms.Select(attrs={'class': ''}),queryset = City.objects.filter(publish=True).order_by('name') , empty_label='Select City')
    
    class Meta:
        model = User
        fields = ['image','video','first_name','last_name','state','city','address','zipcode','mobile','email','yourself','bg_check','available','IsProComplete','IsProCompleteStatus']
    
    def __init__(self, *args, **kwargs):
            super(JobseekerUpdateForm, self).__init__(*args, **kwargs)
            self.fields['mobile'].required                          = True
            self.fields['address'].required                         = True
            self.fields['zipcode'].required                         = True
            self.fields['mobile'].widget.attrs['placeholder']       = 'Enter a Phone #'
            self.fields['email'].widget.attrs['placeholder']        = 'Enter a Email Address'
            self.fields['mobile'].label                             = 'Phone #'
            self.fields['image'].label                              = 'Upload Profile Picture'
            self.fields['video'].label                              = 'Upload Video Resume'
            self.fields['yourself'].label                           = 'Tell employers a little about yourself'
            self.fields['bg_check'].label                           = 'Are you willing to do a background check'
            self.fields['available'].label                          = 'Mark yourself available so employers can hire you'
            self.fields['IsProComplete'].label                      = 'Is Profile Complete'
            self.fields['IsProCompleteStatus'].label                = 'Is Profile Complete Status'
            
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#jobseeker List Filter
class JobseekerListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Email/Name or Phone'}),)
    is_active   = forms.ChoiceField(required=False, label='Actived',choices=[('', '--- Select Activated --')] + [(False,'No'),(True,'Yes'),])
    available   = forms.ChoiceField(required=False, label='Available',choices=[('', '--- Select Available --')] + [(False,'No'),(True,'Yes'),])

#jobseeker schedule update form
class JobseekerScheduleForm(ModelForm):
    
    check_all = forms.BooleanField(required=False,)

    class Meta:
        model = Schedule
        fields = ['user','check_all',
                    'mon','mon_start_hr','mon_start_ap','mon_end_hr','mon_end_ap',
                    'tue','tue_start_hr','tue_start_ap','tue_end_hr','tue_end_ap',
                    'wed','wed_start_hr','wed_start_ap','wed_end_hr','wed_end_ap',
                    'thu','thu_start_hr','thu_start_ap','thu_end_hr','thu_end_ap',
                    'fri','fri_start_hr','fri_start_ap','fri_end_hr','fri_end_ap',
                    'sat','sat_start_hr','sat_start_ap','sat_end_hr','sat_end_ap',
                    'sun','sun_start_hr','sun_start_ap','sun_end_hr','sun_end_ap',
                    'part_time','full_time']
    
    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(JobseekerScheduleForm, self).__init__(*args, **kwargs)
            self.fields['user'].initial   = user
            self.fields['user'].widget  = forms.HiddenInput()

            self.fields['check_all'].label            = 'Check All'
            
            self.fields['part_time'].label      = 'Part-Time'
            self.fields['full_time'].label      = 'Full-Time'

            self.fields['sun'].label            = 'Sunday'
            self.fields['sun_start_hr'].label   = 'Start HR'
            self.fields['sun_start_ap'].label   = 'Start AM/PM'
            self.fields['sun_end_hr'].label     = 'End HR'
            self.fields['sun_end_ap'].label     = 'End AM/PM'

            self.fields['mon'].label            = 'Monday'
            self.fields['mon_start_hr'].label   = 'Start HR'
            self.fields['mon_start_ap'].label   = 'Start AM/PM'
            self.fields['mon_end_hr'].label     = 'End HR'
            self.fields['mon_end_ap'].label     = 'End AM/PM'

            self.fields['tue'].label            = 'Tuesday'
            self.fields['tue_start_hr'].label   = 'Start HR'
            self.fields['tue_start_ap'].label   = 'Start AM/PM'
            self.fields['tue_end_hr'].label     = 'End HR'
            self.fields['tue_end_ap'].label     = 'End AM/PM'

            self.fields['wed'].label            = 'Wendsday'
            self.fields['wed_start_hr'].label   = 'Start HR'
            self.fields['wed_start_ap'].label   = 'Start AM/PM'
            self.fields['wed_end_hr'].label     = 'End HR'
            self.fields['wed_end_ap'].label     = 'End AM/PM'

            self.fields['thu'].label            = 'Thursday'
            self.fields['thu_start_hr'].label   = 'Start HR'
            self.fields['thu_start_ap'].label   = 'Start AM/PM'
            self.fields['thu_end_hr'].label     = 'End HR'
            self.fields['thu_end_ap'].label     = 'End AM/PM'

            self.fields['fri'].label            = 'Friday'
            self.fields['fri_start_hr'].label   = 'Start HR'
            self.fields['fri_start_ap'].label   = 'Start AM/PM'
            self.fields['fri_end_hr'].label     = 'End HR'
            self.fields['fri_end_ap'].label     = 'End AM/PM'

            self.fields['sat'].label            = 'Saturday'
            self.fields['sat_start_hr'].label   = 'Start HR'
            self.fields['sat_start_ap'].label   = 'Start AM/PM'
            self.fields['sat_end_hr'].label     = 'End HR'
            self.fields['sat_end_ap'].label     = 'End AM/PM'

#category List Filter
class CategoryListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])
           
#category create form
class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['name',]
    
    def __init__(self, *args, **kwargs):
            super(CategoryForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#subcategory List Filter
class SubCategoryListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])
    category    = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': ''}),queryset = Category.objects.filter(publish=True).order_by('name') , empty_label='Select Category')
           
#subcategory create form
class SubCategoryForm(ModelForm):

    class Meta:
        model = Subcategory
        fields = ['category','name',]
    
    def __init__(self, *args, **kwargs):
            super(SubCategoryForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
            
#state List Filter
class StateListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])
           
#state create form
class StateForm(ModelForm):

    class Meta:
        model = State
        fields = ['name','code']
    
    def __init__(self, *args, **kwargs):
            super(StateForm, self).__init__(*args, **kwargs)
            self.fields['code'].required = True
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#city List Filter
class CityListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])
    state       = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': ''}),queryset = State.objects.filter(publish=True).order_by('name') , empty_label='Select State')
           
#city create form
class CityForm(ModelForm):

    class Meta:
        model = City
        fields = ['state','name',]
    
    def __init__(self, *args, **kwargs):
            super(CityForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#language List Filter
class LanguageListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])
           
#language create form
class LanguageForm(ModelForm):

    class Meta:
        model   = Language
        fields  = ['name',]
    
    def __init__(self, *args, **kwargs):
            super(LanguageForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#Plan List Filter
class PlanListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])
           
#Plan create form
class PlanForm(ModelForm):

    class Meta:
        model   = Plan
        fields  = ['productid','name','period','amount','info']
    
    def __init__(self, *args, **kwargs):
            super(PlanForm, self).__init__(*args, **kwargs)
            self.fields['info'].widget.attrs['rows'] = 3
            self.fields['productid'].required = True
            self.fields['productid'].label = 'Product ID(Stripe)'

            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#Subscription List Filter
class SubscriptionListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name'}),)
    active      = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])
    plan        = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': ''}),queryset = Plan.objects.filter(publish=True).order_by('name') , empty_label='Select Plan')

#Subscription create form
class SubscriptionCreateForm(ModelForm):
    user        = forms.ModelChoiceField(widget=forms.Select(attrs={'class': ''}),queryset = User.objects.filter(is_staff=False, is_superuser=False, groups__name='Employer').order_by('company') , empty_label='Select Company')
    class Meta:
        model   = Subscription
        fields  = ['user','plan','startdate','enddate','payment_amount']
    
    def __init__(self, *args, **kwargs):
            super(SubscriptionCreateForm, self).__init__(*args, **kwargs)
            self.fields['user'].label                               = 'Employer'
            self.fields['startdate'].required                       = True
            self.fields['startdate'].widget.attrs['readonly']       = True
            self.fields['enddate'].required                         = True
            self.fields['enddate'].widget.attrs['readonly']         = True
            self.fields['payment_amount'].required                  = True
            self.fields['payment_amount'].widget.attrs['readonly']  = True
            self.fields['payment_amount'].label                     = 'Amount'
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#Subscription create form
class SubscriptionUpdateForm(ModelForm):
    
    class Meta:
        model   = Subscription
        fields  = ['user','plan','startdate','enddate','payment_amount','payment_type','payment_status','expired']
    
    def __init__(self, *args, **kwargs):
            super(SubscriptionUpdateForm, self).__init__(*args, **kwargs)
            self.fields['user'].widget  = forms.HiddenInput()
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#Job List Filter
class JobListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Title'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])

#Job create form
class JobCreateForm(ModelForm):
    user        = forms.ModelChoiceField(widget=forms.Select(attrs={'class': ''}),queryset = User.objects.filter(is_staff=False, is_superuser=False, groups__name='Employer').order_by('company') , empty_label='Select Company')
    class Meta:
        model   = Job
        fields  = ['user','hiring_manager_name','hiring_company','email','phone','title','description','state','city','address','zipcode','category','subcategory','hourly_rate','number_of_roles']
    
    def __init__(self, *args, **kwargs):
            super(JobCreateForm, self).__init__(*args, **kwargs)

            if self.instance.id:
                self.fields['user'].widget        = forms.HiddenInput()
            else:
                self.fields['user'].label          = 'Employer'
            
            self.fields['hiring_manager_name'].label = 'Hiring Manager Name'
            self.fields['hiring_company'].label      = 'Company Name'
            self.fields['title'].label               = 'Job Title'
            self.fields['description'].label         = 'Job Description'
            self.fields['description'].required      = True
            self.fields['description'].widget.attrs['rows'] = 3
            self.fields['address'].label             = 'Job Street'
            self.fields['state'].label               = 'Job State'
            self.fields['city'].label                = 'Job City'
            self.fields['zipcode'].label             = 'Job Zipcode'
            self.fields['category'].label            = 'Job Category'
            self.fields['subcategory'].label         = 'Job Sub Categories'
            self.fields['hourly_rate'].label         = 'Hourly Pay Rate'

            self.fields['number_of_roles'].required  = True
            self.fields['number_of_roles'].label     = '# of Roles'

            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#Job jobseeker List Filter
class JobJobseekerListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Email/Name or Phone'}),)
    available   = forms.ChoiceField(required=False, label='Available',choices=[('', '--- Select Available --')] + [(False,'No'),(True,'Yes'),])
    category    = forms.ModelChoiceField(required=False, widget=forms.Select(attrs={'class': ''}),queryset = Category.objects.filter(publish=True).order_by('name') , empty_label='Select Category')

#Job schedule update form
class JobScheduleForm(forms.ModelForm):
    
    check_all = forms.BooleanField(required=False,)

    class Meta:
        model = JobShiftSchedule
        fields = ['job','check_all','startdate','enddate',
                    'mon','mon_start_hr','mon_start_ap','mon_end_hr','mon_end_ap',
                    'tue','tue_start_hr','tue_start_ap','tue_end_hr','tue_end_ap',
                    'wed','wed_start_hr','wed_start_ap','wed_end_hr','wed_end_ap',
                    'thu','thu_start_hr','thu_start_ap','thu_end_hr','thu_end_ap',
                    'fri','fri_start_hr','fri_start_ap','fri_end_hr','fri_end_ap',
                    'sat','sat_start_hr','sat_start_ap','sat_end_hr','sat_end_ap',
                    'sun','sun_start_hr','sun_start_ap','sun_end_hr','sun_end_ap',
                    ]
    
    def __init__(self, *args, **kwargs):
            job = kwargs.pop('job', None)
            super(JobScheduleForm, self).__init__(*args, **kwargs)
            self.fields['job'].initial      = job
            self.fields['job'].widget       = forms.HiddenInput()
            
            self.fields['startdate'].required = True
            self.fields['enddate'].required   = True

            self.fields['check_all'].label            = 'Check All'

            self.fields['sun'].label            = 'Sunday'
            self.fields['sun_start_hr'].label   = 'Start HR'
            self.fields['sun_start_ap'].label   = 'Start AM/PM'
            self.fields['sun_end_hr'].label     = 'End HR'
            self.fields['sun_end_ap'].label     = 'End AM/PM'

            self.fields['mon'].label            = 'Monday'
            self.fields['mon_start_hr'].label   = 'Start HR'
            self.fields['mon_start_ap'].label   = 'Start AM/PM'
            self.fields['mon_end_hr'].label     = 'End HR'
            self.fields['mon_end_ap'].label     = 'End AM/PM'

            self.fields['tue'].label            = 'Tuesday'
            self.fields['tue_start_hr'].label   = 'Start HR'
            self.fields['tue_start_ap'].label   = 'Start AM/PM'
            self.fields['tue_end_hr'].label     = 'End HR'
            self.fields['tue_end_ap'].label     = 'End AM/PM'

            self.fields['wed'].label            = 'Wendsday'
            self.fields['wed_start_hr'].label   = 'Start HR'
            self.fields['wed_start_ap'].label   = 'Start AM/PM'
            self.fields['wed_end_hr'].label     = 'End HR'
            self.fields['wed_end_ap'].label     = 'End AM/PM'

            self.fields['thu'].label            = 'Thursday'
            self.fields['thu_start_hr'].label   = 'Start HR'
            self.fields['thu_start_ap'].label   = 'Start AM/PM'
            self.fields['thu_end_hr'].label     = 'End HR'
            self.fields['thu_end_ap'].label     = 'End AM/PM'

            self.fields['fri'].label            = 'Friday'
            self.fields['fri_start_hr'].label   = 'Start HR'
            self.fields['fri_start_ap'].label   = 'Start AM/PM'
            self.fields['fri_end_hr'].label     = 'End HR'
            self.fields['fri_end_ap'].label     = 'End AM/PM'

            self.fields['sat'].label            = 'Saturday'
            self.fields['sat_start_hr'].label   = 'Start HR'
            self.fields['sat_start_ap'].label   = 'Start AM/PM'
            self.fields['sat_end_hr'].label     = 'End HR'
            self.fields['sat_end_ap'].label     = 'End AM/PM'

#blog category List Filter
class BlogCategoryListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])

#blog category List Filter
class ContactUsListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Name, Email and Phone'}),)

#blog category create form
class BlogCategoryForm(ModelForm):

    class Meta:
        model = BlogCategory
        fields = ['name',]
    
    def __init__(self, *args, **kwargs):
            super(BlogCategoryForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'

#Blog List Filter
class BlogListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Title'}),)
    publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])

#Blog create form
class BlogCreateForm(ModelForm):
    class Meta:
        model   = Blog
        fields  = ['image','title','category','description',]
    
    def __init__(self, *args, **kwargs):
            super(BlogCreateForm, self).__init__(*args, **kwargs)
            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control'
