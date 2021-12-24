from django.contrib import admin
from django.contrib.auth.admin import   UserAdmin as DjangoAdminUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from accountapp.models import *

# Admin Headers
admin.site.site_header = 'Go To Work America Admin'
admin.site.site_title = 'Go To Work America Admin'
#admin.site.site_url = 'https://www.hobbyideas.in'
admin.site.index_title = 'Go To Work America Administration'
admin.empty_value_display = '**Empty**'

#admin users
class UserAdmin(BaseUserAdmin):
    
    list_display = ('date_joined','first_name','last_name','email','mobile','is_staff')
    list_filter = ('groups', 'date_joined','is_staff', 'state', 'city','language')
    fieldsets = (
        (None, {'fields': ('company','title','first_name', 'last_name', 'email', 'mobile', 'password', 'state', 'city', 'address', 'zipcode','language','yourself','bg_check','image','video','available','IsProComplete','IsProCompleteStatus')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'IsVerified', 'groups', 'user_permissions',)}),
        ('Other Information', {'fields': ('source', 'ipaddress', 'browserinfo','device_id','devicetoken')}),

    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'company','title','first_name','last_name','email','mobile','state','city','address','zipcode','language','yourself','bg_check','image','video','available','IsProComplete','IsProCompleteStatus','password1','password2',
                )
            }
        ),
    )
    search_fields       = ('first_name','last_name', 'email', 'mobile')
    ordering            = ('-date_joined',)

admin.site.register(User, UserAdmin)
admin.site.register(State)
admin.site.register(City)
admin.site.register(Language)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(UserCategory)
admin.site.register(Schedule)
admin.site.register(Plan)
admin.site.register(Subscription)
admin.site.register(TemporaryPassword)
admin.site.register(Notification)
admin.site.register(AdminNotification)
admin.site.register(ContactUs)
admin.site.register(Newsletter)