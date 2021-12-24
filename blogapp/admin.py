from django.contrib import admin
from blogapp.models import *

admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(BlogView)
admin.site.register(BlogComment)

# Register your models here.
