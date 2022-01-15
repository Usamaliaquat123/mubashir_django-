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

#Job List Filter
class JobListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Job Title, Company & Email'}),)
    #publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])

#Job List Filter
class JobOffersListFilter(forms.Form):
    search      = forms.CharField(required=False, label='Search',widget=TextInput(attrs={'placeholder': 'Search by Job Title, Jobseeker Name, Jobseeker Email & Jobseeker Phone'}),)
    #publish     = forms.ChoiceField(required=False, label='Active',choices=[('', '--- Select Active --')] + [(False,'No'),(True,'Yes'),])

#Job create form
class JobCreateForm(ModelForm):

    city        = forms.ModelChoiceField(queryset=City.objects.none())
    subcategory = forms.ModelMultipleChoiceField(queryset=Subcategory.objects.none())

    class Meta:
        model   = Job
        fields  = ['user','hiring_manager_name','hiring_company','email','phone','title','description','address','state','city','zipcode','category','subcategory','hourly_rate','number_of_roles']
    
    def __init__(self, *args, **kwargs):
            user        = kwargs.pop('user', None)
            super(JobCreateForm, self).__init__(*args, **kwargs)
            self.fields['user'].initial              = user
            self.fields['user'].widget               = forms.HiddenInput()
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
            self.fields['hourly_rate'].label         = 'Hourly'
            self.fields['number_of_roles'].required  = True
            self.fields['number_of_roles'].label     = 'Roles'
    
            self.fields['subcategory'].queryset = Subcategory.objects.none()
            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['subcategory'].queryset = Subcategory.objects.filter(category=category_id, publish=True).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['subcategory'].queryset = self.instance.category.subcategory_set.order_by('name')
            
            self.fields['city'].queryset = City.objects.none()
            if 'state' in self.data:
                try:
                    state_id = int(self.data.get('state'))
                    self.fields['city'].queryset = City.objects.filter(state=state_id, publish=True).order_by('name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['city'].queryset = self.instance.state.city_set.order_by('name')

            for field in self.fields.values():
                field.widget.attrs['class'] = 'form-control bgColorJumbotron'

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
            
            self.fields['check_all'].label            = 'Check All'
            
            self.fields['startdate'].required = True
            self.fields['enddate'].required   = True
            
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

            self.fields['sun'].label            = 'Sunday'
            self.fields['sun_start_hr'].label   = 'Start HR'
            self.fields['sun_start_ap'].label   = 'Start AM/PM'
            self.fields['sun_end_hr'].label     = 'End HR'
            self.fields['sun_end_ap'].label     = 'End AM/PM'
    
    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        mon = self.cleaned_data.get('mon')
        if mon:
            start_hr    = self.cleaned_data.get('mon_start_hr')
            start_ap    = self.cleaned_data.get('mon_start_ap')
            end_hr      = self.cleaned_data.get('mon_end_hr')
            end_ap      = self.cleaned_data.get('mon_end_ap')
            if start_hr == '':
                raise ValidationError( "Please select Monday Start HR" )
            if start_ap is None:
                raise ValidationError( "Please select Monday Start AM/PM" )
            if end_hr is None:
                raise ValidationError( "Please select Monday End HR" )
            if end_ap is None:
                raise ValidationError( "Please select Monday End AM/PM" )

        tue = self.cleaned_data.get('tue')
        if tue:
            start_hr    = self.cleaned_data.get('tue_start_hr')
            start_ap    = self.cleaned_data.get('tue_start_ap')
            end_hr      = self.cleaned_data.get('tue_end_hr')
            end_ap      = self.cleaned_data.get('tue_end_ap')
            if start_hr == '':
                raise ValidationError( "Please select Tuesday Start HR" )
            if start_ap is None:
                raise ValidationError( "Please select Tuesday Start AM/PM" )
            if end_hr is None:
                raise ValidationError( "Please select Tuesday End HR" )
            if end_ap is None:
                raise ValidationError( "Please select Tuesday End AM/PM" )
        
        wed = self.cleaned_data.get('wed')
        if wed:
            start_hr    = self.cleaned_data.get('wed_start_hr')
            start_ap    = self.cleaned_data.get('wed_start_ap')
            end_hr      = self.cleaned_data.get('wed_end_hr')
            end_ap      = self.cleaned_data.get('wed_end_ap')
            if start_hr == '':
                raise ValidationError( "Please select Wendsday Start HR" )
            if start_ap is None:
                raise ValidationError( "Please select Wendsday Start AM/PM" )
            if end_hr is None:
                raise ValidationError( "Please select Wendsday End HR" )
            if end_ap is None:
                raise ValidationError( "Please select Wendsday End AM/PM" )
        
        thu = self.cleaned_data.get('thu')
        if thu:
            start_hr    = self.cleaned_data.get('thu_start_hr')
            start_ap    = self.cleaned_data.get('thu_start_ap')
            end_hr      = self.cleaned_data.get('thu_end_hr')
            end_ap      = self.cleaned_data.get('thu_end_ap')
            if start_hr == '':
                raise ValidationError( "Please select Thursday Start HR" )
            if start_ap is None:
                raise ValidationError( "Please select Thursday Start AM/PM" )
            if end_hr is None:
                raise ValidationError( "Please select Thursday End HR" )
            if end_ap is None:
                raise ValidationError( "Please select Thursday End AM/PM" )

        fri = self.cleaned_data.get('fri')
        if fri:
            start_hr    = self.cleaned_data.get('fri_start_hr')
            start_ap    = self.cleaned_data.get('fri_start_ap')
            end_hr      = self.cleaned_data.get('fri_end_hr')
            end_ap      = self.cleaned_data.get('fri_end_ap')
            if start_hr == '':
                raise ValidationError( "Please select Friday Start HR" )
            if start_ap is None:
                raise ValidationError( "Please select Friday Start AM/PM" )
            if end_hr is None:
                raise ValidationError( "Please select Friday End HR" )
            if end_ap is None:
                raise ValidationError( "Please select Friday End AM/PM" )

        sat = self.cleaned_data.get('sat')
        if sat:
            start_hr    = self.cleaned_data.get('sat_start_hr')
            start_ap    = self.cleaned_data.get('sat_start_ap')
            end_hr      = self.cleaned_data.get('sat_end_hr')
            end_ap      = self.cleaned_data.get('sat_end_ap')
            if start_hr == '':
                raise ValidationError( "Please select Saturday Start HR" )
            if start_ap is None:
                raise ValidationError( "Please select Saturday Start AM/PM" )
            if end_hr is None:
                raise ValidationError( "Please select Saturday End HR" )
            if end_ap is None:
                raise ValidationError( "Please select Saturday End AM/PM" )
        
        sun = self.cleaned_data.get('sun')
        if sun:
            start_hr    = self.cleaned_data.get('sun_start_hr')
            start_ap    = self.cleaned_data.get('sun_start_ap')
            end_hr      = self.cleaned_data.get('sun_end_hr')
            end_ap      = self.cleaned_data.get('sun_end_ap')
            if start_hr == '':
                raise ValidationError( "Please select Sunday Start HR" )
            if start_ap is None:
                raise ValidationError( "Please select Sunday Start AM/PM" )
            if end_hr is None:
                raise ValidationError( "Please select Sunday End HR" )
            if end_ap is None:
                raise ValidationError( "Please select Sunday End AM/PM" )

        return cleaned_data

#Job Offer form
class JobOfferForm(ModelForm):
    class Meta:
        model   = JobOffer
        fields  = ['contacted','rating','showed_up']

    def __init__(self, *args, **kwargs):

        super(JobOfferForm, self).__init__(*args, **kwargs)
        self.fields['contacted'].label      = 'Contacted?'
        self.fields['rating'].label         = 'Rating(%)'
        self.fields['showed_up'].label      = 'Showed Up?'
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if rating:
            if rating > 100:
                raise ValidationError('Rating should be less than or equal to 100.')
        return rating