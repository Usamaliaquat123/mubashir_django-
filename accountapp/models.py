from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
import uuid
from autoslug import AutoSlugField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
import select2.fields
import select2.models
from django.contrib.postgres.fields import JSONField

#User Manager Overrite
class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True")
        return self._create_user(email, password, **extra_fields)

#States
class State(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    name        = models.CharField(max_length=255, unique=True)
    code        = models.CharField(max_length=255, null=True, blank=True)
    publish     = models.BooleanField(default = True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

#Cities
class City(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    state       = models.ForeignKey(State, on_delete=models.CASCADE)
    name        = models.CharField(max_length=255)
    publish     = models.BooleanField(default = True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

#Language
class Language(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    name        = models.CharField(max_length=55, unique=True)
    code        = models.CharField(max_length=5, unique=True)
    publish     = models.BooleanField(default = True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

#Categories
class Category(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    name        = models.CharField(max_length=255, unique=True)
    slug        = AutoSlugField(populate_from='name', always_update=True, unique=True)
    publish     = models.BooleanField(default = True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

#Cities
class Subcategory(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    category    = models.ForeignKey(Category, on_delete=models.CASCADE)
    name        = models.CharField(max_length=255)
    slug        = AutoSlugField(populate_from='name', always_update=True, unique=True)
    publish     = models.BooleanField(default = True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt   = models.DateTimeField(auto_now=True, null=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'

#User Model Overrite
class User(AbstractUser):
    token               = models.UUIDField(default= uuid.uuid4, unique=True)
    email               = models.EmailField(_('email address'), unique=True)
    username            = None
    mobile              = models.CharField(max_length=255, unique=True, null=True, blank=True)
    state               = models.ForeignKey(State, on_delete=models.CASCADE, null=True, blank=True)
    city                = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    address             = models.CharField(max_length=255, null=True, blank=True)
    zipcode             = models.CharField(max_length=255, null=True, blank=True)
    latitude            = models.FloatField(null=True,blank=True)
    longitude           = models.FloatField(null=True,blank=True)
    language            = models.ManyToManyField(Language, null=True, blank=True)
    yourself            = models.TextField(null=True, blank=True)
    bg_check            = models.CharField(max_length=10, choices=(('Yes','Yes'),('No','No')), null=True, blank=True)
    image               = models.ImageField(null=True, blank=True, upload_to="users/images/", validators=[FileExtensionValidator(allowed_extensions=['JPG','JPEG','PNG','jpg','jpeg','png'])])
    video               = models.FileField(null=True, blank=True, upload_to="users/videos/", validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])])
    available           = models.BooleanField(default = False)
    company             = models.CharField(max_length=255, null=True, blank=True)
    title               = models.CharField(max_length=255, null=True, blank=True)
    IsProComplete       = models.BooleanField(default=False)
    IsProCompleteStatus = models.CharField(max_length=15, choices=(('Register','Register'),('Contact','Contact'),('Category','Category'),('Schedule','Schedule'),('Video','Video'),('Image','Image'),('Complete','Complete')),  default='Register')
    IsVerified          = models.BooleanField(default=False)
    ipaddress           = models.GenericIPAddressField(null=True, blank=True)
    source              = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo         = models.TextField(null=True, blank=True)
    updatedAt           = models.DateTimeField(auto_now=True, null=True)
    createdBy           = select2.fields.ForeignKey('self',ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='user_created_by', null=True, blank=True)
    device_id           = models.TextField(null=True, blank=True)
    devicetoken         = models.TextField(null=True, blank=True)


    USERNAME_FIELD      = 'email'
    REQUIRED_FIELDS     = []

    object = UserManager()

    def __int__(self):
        return self.id
    
    def __str__(self):
        if self.company:
            return self.company
        elif self.first_name:
            return str(self.first_name)+' - '+str(self.last_name)
        else:
            return self.email
    
    def get_admin_url(self):
        """the url to the Django admin interface for the model instance"""
        from django.urls import reverse
        info = (self._meta.app_label, self._meta.model_name)
        return reverse('admin:%s_%s_change' % info, args=(self.pk,))

#Profile Views
class UserProfileView(models.Model):
    id          = models.BigAutoField(primary_key=True)
    user        = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, null=True, blank=True)
    viewby      = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='profile_view_by', null=True, blank=True)
    ipaddress   = models.GenericIPAddressField(null=True, blank=True)
    source      = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo = models.TextField(null=True, blank=True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    
    def __int__(self):
        return self.id

    class Meta:
        verbose_name        = "User Profile View"
        verbose_name_plural = "User Profile Views"

#User Selected Categroies
class UserCategory(models.Model):
    user            = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory     = models.ManyToManyField(Subcategory, null=True, blank=True)
    createdAt       = models.DateTimeField(auto_now_add=True, null=True)
    
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return str(self.user.email)+' - '+str(self.category.name)

    class Meta:
        verbose_name = 'User Category'
        verbose_name_plural = 'User Categories'

#User Schedule
class Schedule(models.Model):
    token           = models.UUIDField(default= uuid.uuid4, unique=True)
    user            = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE)
    sun             = models.BooleanField(default = False)
    sun_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    sun_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    sun_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    sun_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    mon             = models.BooleanField(default = False)
    mon_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    mon_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    mon_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    mon_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    tue             = models.BooleanField(default = False)
    tue_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    tue_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    tue_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    tue_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    wed             = models.BooleanField(default = False)
    wed_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    wed_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    wed_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    wed_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    thu             = models.BooleanField(default = False)
    thu_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    thu_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    thu_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    thu_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    fri             = models.BooleanField(default = False)
    fri_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    fri_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    fri_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    fri_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    sat             = models.BooleanField(default = False)
    sat_start_hr    = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    sat_start_ap    = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    sat_end_hr      = models.IntegerField(choices=((1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),(8,8),(9,9),(10,10),(11,11),(12,12)), null=True, blank=True)
    sat_end_ap      = models.CharField(max_length=10, choices=(('AM','AM'),('PM','PM')), null=True, blank=True)
    part_time       = models.BooleanField(default = False)
    full_time       = models.BooleanField(default = False)
    status          = models.CharField(max_length=10, choices=(('Old','Old'),('Current','Current')),  default='Current')
    createdAt       = models.DateTimeField(auto_now_add=True)
    ipaddress       = models.GenericIPAddressField(null=True, blank=True)
    source          = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo     = models.TextField(null=True, blank=True)
    updatedAt       = models.DateTimeField(auto_now=True)
    createdBy       = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='schedule_created_by', null=True, blank=True)

    
    def __int__(self):
        return self.id
    
    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

#Plan
class Plan(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    productid   = models.CharField(max_length=55, null=True, blank=True)
    name        = models.CharField(max_length=255, unique=True)
    period      = models.CharField(max_length=55, choices=(('monthly','Monthly'),('quarterly','Quarterly'),('half-yearly','Half Yearly'),('yearly','Yearly')),  default='monthly')
    amount      = models.IntegerField()
    info        = models.TextField(null=True, blank=True)
    unlimited   = models.BooleanField(default = True)
    noofjob     = models.IntegerField(null=True, blank=True)
    noofrequest = models.IntegerField(null=True, blank=True)
    publish     = models.BooleanField(default = True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt   = models.DateTimeField(auto_now=True, null=True)
    createdBy   = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='plan_created_by', null=True, blank=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return str(self.name)+' - '+str(self.get_period_display())

    class Meta:
        verbose_name = 'Plan'
        verbose_name_plural = 'Plans'

#Subscription
class Subscription(models.Model):
    token                   = models.UUIDField(default= uuid.uuid4)
    user                    = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE)
    plan                    = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    period                  = models.CharField(max_length=55, choices=(('monthly','Monthly'),('quarterly','Quarterly'),('half-yearly','Half Yearly'),('yearly','Yearly')),  null=True, blank=True)
    stripeid                = models.CharField(max_length=255, null=True, blank=True)
    stripe_subscription_id  = models.CharField(max_length=255, null=True, blank=True)
    cancel_at_period_end    = models.BooleanField(default=False)
    membership              = models.BooleanField(default=False)
    unlimited               = models.BooleanField(default = True)
    startdate               = models.DateField(null=True, blank=True)
    enddate                 = models.DateField(null=True, blank=True)
    noofjob                 = models.IntegerField(null=True, blank=True)
    noofrequest             = models.IntegerField(null=True, blank=True)
    active                  = models.BooleanField(default = True)
    expired                 = models.BooleanField(default = False)
    recurring               = models.BooleanField(default = True)
    status                  = models.CharField(max_length=10, choices=(('Old','Old'),('Current','Current')),  default='Current')
    payment_amount          = models.IntegerField(null=True, blank=True)
    payment_type            = models.CharField(max_length=55, choices=(('Online','Online'),('Offline','Offline')),  default='Offline')
    payment_status          = models.CharField(max_length=55, choices=(('Success','Success'),('Fail','Fail'),('Pending','Pending')),  default='Pending')
    payment_response        = JSONField(null=True, blank=True)
    ipaddress               = models.GenericIPAddressField(null=True, blank=True)
    source                  = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo             = models.TextField(null=True, blank=True)
    createdAt               = models.DateTimeField(auto_now_add=True)
    updatedAt               = models.DateTimeField(auto_now=True)
    createdBy               = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='subscrption_created_by', null=True, blank=True)
    canceldate              = models.DateTimeField(null=True, blank=True)
    cancel_response         = JSONField(null=True, blank=True)

    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.plan.name

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

#Temporary Password
class TemporaryPassword(models.Model):
    id              = models.BigAutoField(primary_key=True)
    token           = models.UUIDField(default= uuid.uuid4, unique=True)
    device_id       = models.CharField(max_length=255, null=True, blank=True)
    user            = models.ForeignKey(User,on_delete=models.CASCADE)
    password        = models.CharField(max_length=6)
    isUsed          = models.BooleanField(default = False)
    isExpired       = models.BooleanField(default = False)
    ipaddress       = models.GenericIPAddressField(null=True, blank=True)
    source          = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo     = models.TextField(null=True, blank=True)
    createdAt       = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt       = models.DateTimeField(auto_now=True, null=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return str(self.user.email)+' - '+str(self.password)

    class Meta:
        verbose_name        = "Temporary Password"
        verbose_name_plural = "Temporary Passwords"

#Admin Notification
class AdminNotification(models.Model):
    id              = models.BigAutoField(primary_key=True)
    token           = models.UUIDField(default= uuid.uuid4, unique=True)
    message         = models.TextField()
    isRead          = models.BooleanField(default = False)
    createdAt       = models.DateTimeField(auto_now_add=True, null=True)
    updatedAt       = models.DateTimeField(auto_now=True, null=True)
    createdBy       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_notification_created_by', null=True, blank=True)
    readBy          = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.message

    class Meta:
        verbose_name        = "Admin Notification"
        verbose_name_plural = "Admin Notifications"

#Notification
class Notification(models.Model):
    id              = models.BigAutoField(primary_key=True)
    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    message         = models.TextField()
    isRead          = models.BooleanField(default = False)
    createdAt       = models.DateTimeField(auto_now_add=True, null=True)
    createdBy       = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_created_by', null = True, blank = True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.message

    class Meta:
        verbose_name        = "Notification"
        verbose_name_plural = "Notifications"

#Contact us
class ContactUs(models.Model):
    user        = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, null=True, blank=True)
    name        = models.CharField(max_length=255)
    email       = models.EmailField(_('email address'))
    phone       = models.CharField(max_length=255)
    message     = models.TextField(null=True, blank=True)
    ipaddress   = models.GenericIPAddressField(null=True, blank=True)
    source      = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo = models.TextField(null=True, blank=True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    
    def __int__(self):
        return self.id
    
    class Meta:
        verbose_name        = "Contact Us"
        verbose_name_plural = "Contact Us"

#newsletter
class Newsletter(models.Model):
    user        = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, null=True, blank=True)
    name        = models.CharField(max_length=255)
    email       = models.EmailField(_('email address'), unique=True)
    ipaddress   = models.GenericIPAddressField(null=True, blank=True)
    source      = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo = models.TextField(null=True, blank=True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    
    def __int__(self):
        return self.id
    
    class Meta:
        verbose_name        = "Newsletter"
        verbose_name_plural = "Newsletters"
