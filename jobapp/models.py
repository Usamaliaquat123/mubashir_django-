from django.db import models
import uuid
from accountapp.models import *
from autoslug import AutoSlugField
from django.core.validators import FileExtensionValidator
import select2.fields
import select2.models

#Job
class Job(models.Model):
    token               = models.UUIDField(default= uuid.uuid4)
    user                = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE)
    hiring_manager_name = models.CharField(max_length=255)
    hiring_company      = models.CharField(max_length=255)
    email               = models.EmailField(max_length=255)
    phone               = models.CharField(max_length=255)
    title               = models.CharField(max_length=255)
    slug                = AutoSlugField(populate_from='title', always_update=True, unique=True)
    description         = models.TextField(null=True, blank=True)
    detail              = models.TextField(null=True, blank=True)
    state               = models.ForeignKey(State, on_delete=models.CASCADE)
    city                = models.ForeignKey(City, on_delete=models.CASCADE)
    address             = models.CharField(max_length=255)
    zipcode             = models.CharField(max_length=255)
    latitude            = models.FloatField(null=True,blank=True)
    longitude           = models.FloatField(null=True,blank=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory         = models.ManyToManyField(Subcategory)
    hourly_rate         = models.IntegerField()
    number_of_roles     = models.IntegerField(null=True, blank=True)
    publish             = models.BooleanField(default = True)
    IsDeleted           = models.BooleanField(default = False)
    ipaddress           = models.GenericIPAddressField(null=True, blank=True)
    source              = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo         = models.TextField(null=True, blank=True)
    createdAt           = models.DateTimeField(auto_now_add=True)
    updatedAt           = models.DateTimeField(auto_now=True)
    subscription        = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    createdBy           = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='job_created_by', null=True, blank=True)

    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'

#Job Shift Schedule
class JobShiftSchedule(models.Model):
    token           = models.UUIDField(default= uuid.uuid4, unique=True)
    job             = models.OneToOneField(Job, on_delete=models.CASCADE)
    startdate       = models.DateField(null=True, blank=True)
    enddate         = models.DateField(null=True, blank=True)
    sun             = models.BooleanField(default = False)
    sun_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), default=6)
    sun_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    sun_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    sun_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    mon             = models.BooleanField(default = False)
    mon_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), default=6)
    mon_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    mon_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    mon_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    tue             = models.BooleanField(default = False)
    tue_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), default=6)
    tue_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    tue_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    tue_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    wed             = models.BooleanField(default = False)
    wed_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), default=6)
    wed_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    wed_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    wed_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    thu             = models.BooleanField(default = False)
    thu_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), default=6)
    thu_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    thu_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    thu_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    fri             = models.BooleanField(default = False)
    fri_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), default=6)
    fri_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    fri_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True,)
    fri_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    sat             = models.BooleanField(default = False)
    sat_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), default=6)
    sat_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    sat_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    sat_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    createdAt       = models.DateTimeField(auto_now_add=True)
    ipaddress       = models.GenericIPAddressField(null=True, blank=True)
    source          = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo     = models.TextField(null=True, blank=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    createdBy       = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='job_shift_schedule_created_by', null=True, blank=True)
    
    def __int__(self):
        return self.id
    
    class Meta:
        verbose_name = 'Job Shift Schedule'
        verbose_name_plural = 'Job Shift Schedules'

#Job Offers
class JobOffer(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    token               = models.UUIDField(default= uuid.uuid4)
    user                = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE)
    job                 = models.ForeignKey(Job, on_delete=models.CASCADE)
    instruction         = models.TextField(null=True, blank=True)
    action              = models.CharField(max_length=25, choices=(('Pending','Pending'),('Accept','Accept'),('Decline','Decline')),  default='Pending')
    isPayrollService    = models.BooleanField(default = False)
    contacted           = models.BooleanField(default = False)
    rating              = models.IntegerField(null=True, blank=True)
    showed_up           = models.CharField(max_length=10, choices=(('Yes','Yes'),('No','No')), null=True, blank=True)
    ipaddress           = models.GenericIPAddressField(null=True, blank=True)
    source              = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo         = models.TextField(null=True, blank=True)
    createdAt           = models.DateTimeField(auto_now_add=True)
    updatedAt           = models.DateTimeField(auto_now=True)
    subscription        = models.ForeignKey(Subscription, on_delete=models.CASCADE, null=True, blank=True)
    createdBy           = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='job_offer_created_by', null=True, blank=True)
    IsRead              = models.BooleanField(default = False)
    read_ipaddress      = models.GenericIPAddressField(null=True, blank=True)
    read_source         = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    read_browserinfo    = models.TextField(null=True, blank=True)
    read_datetime       = models.DateTimeField(null=True, blank=True)
    read_by             = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='job_offer_read_by', null=True, blank=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return str(self.user.first_name)+' '+str(self.user.last_name)+' - '+str(self.job.title)+' - '+str(self.action)

    class Meta:
        verbose_name = 'Job Offer'
        verbose_name_plural = 'Job Offers'

#Job Offer Action
class JobOfferAction(models.Model):
    id                  = models.BigAutoField(primary_key=True)
    token               = models.UUIDField(default= uuid.uuid4)
    user                = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE)
    joboffer            = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    action              = models.CharField(max_length=25)
    ipaddress           = models.GenericIPAddressField(null=True, blank=True)
    source              = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo         = models.TextField(null=True, blank=True)
    createdAt           = models.DateTimeField(auto_now_add=True)
    updatedAt           = models.DateTimeField(auto_now=True)
    createdBy           = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='job_offer_action_created_by', null=True, blank=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return str(self.user.first_name)+' '+str(self.user.last_name)+' - '+str(self.joboffer.job.title)+' - '+str(self.action)

    class Meta:
        verbose_name = 'Job Action'
        verbose_name_plural = 'Job Actions'
