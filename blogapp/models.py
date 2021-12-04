from django.db import models
from django.forms import ModelForm
from accountapp.models import *
import uuid
import datetime # for date field
from autoslug import AutoSlugField
from django.utils.safestring import mark_safe
import select2.fields
import select2.models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.core import serializers

#Categories
class BlogCategory(models.Model):
    name        = models.CharField(max_length=255, unique=True)
    slug        = AutoSlugField(populate_from='name', always_update=True, unique=True)
    publish     = models.BooleanField(default = True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

#Blog
class Blog(models.Model):
    token       = models.UUIDField(default= uuid.uuid4)
    image       = models.ImageField(null=True, blank=True, upload_to="blog/images/")
    title       = models.CharField(max_length=255)
    slug        = AutoSlugField(populate_from='title', always_update=True, unique=True)
    category    = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    description = RichTextUploadingField()
    featured    = models.BooleanField(default=False)
    publish     = models.BooleanField(default = False) #used for approval / disapproval - default disapproved
    ipaddress   = models.GenericIPAddressField(null=True, blank=True)
    source      = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  blank = True, null=True)  
    browserinfo = models.TextField(null=True, blank=True)
    createdAt   = models.DateTimeField(auto_now_add=True,)
    updatedAt   = models.DateTimeField(auto_now=True)
    createdBy   = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, related_name='blog_created_by', null=True, blank=True)
    
    def __int__(self):
        return self.id
    
    def __str__(self):
        return self.title

    def image_tag(self):
        # return mark_safe('<img src="{url}" width="{width}" height={height} />'.format(
        return mark_safe('<a href="{url}" target="_blank">{url}</a>'.format(
            url = self.image.url,
            # width=self.image.width,
            # height=self.image.height,
            )
    )
    image_tag.short_description = 'Uploaded Image'
		
    class Meta:
        verbose_name        = "Blog"
        verbose_name_plural = "Blogs"

#Blog Views
class BlogView(models.Model):
    id          = models.BigAutoField(primary_key=True)
    user        = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE, null=True, blank=True)
    blog        = models.ForeignKey(Blog, on_delete=models.CASCADE)
    ipaddress   = models.GenericIPAddressField(null=True, blank=True)
    source      = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo = models.TextField(null=True, blank=True)
    createdAt   = models.DateTimeField(auto_now_add=True,null=True)
    
    def __int__(self):
        return self.id

    class Meta:
        verbose_name        = "View"
        verbose_name_plural = "Views"

#Blog Comments
class BlogComment(models.Model):
    id          = models.BigAutoField(primary_key=True)
    user        = select2.fields.ForeignKey(User,ajax=True, search_field='email', overlay="Choose an user...",js_options={'quiet_millis': 10,}, on_delete=models.CASCADE)
    blog        = models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment     = models.TextField()
    ipaddress   = models.GenericIPAddressField(null=True, blank=True)
    source      = models.CharField(max_length=10, choices=(('IOS','IOS'),('Android','Android'),('Web','Web')),  default='Web')
    browserinfo = models.TextField(null=True, blank=True)
    createdAt   = models.DateTimeField(auto_now_add=True, null=True)
    
    def __int__(self):
        return self.id

    class Meta:
        verbose_name        = "Comment"
        verbose_name_plural = "Comments"
