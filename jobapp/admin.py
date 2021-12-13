from django.contrib import admin
from django import forms
from jobapp.models import *

admin.site.register(Job)
admin.site.register(JobShiftSchedule)
admin.site.register(JobOffer)
admin.site.register(JobOfferAction)