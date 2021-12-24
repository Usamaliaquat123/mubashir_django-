from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import  HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.cache  import cache_control
from accountapp.models import *
from backendapp.forms import *
from apiapp.models import *
from backendapp.decorator import check_role_permission
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import resolve
import logging
db_logger = logging.getLogger('backendapp')

#apikey listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apikey_list(request, template_name='backend/apikey/list.html'):
    try:
        data = {}
        records             = APIAuthKey.objects.all().order_by('-createdAt')
        data['object_list'] = records
        return render(request, template_name, data)
    except Exception as e:
            db_logger.exception(e)
            return e

#apikey status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apikey_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            records = APIAuthKey.objects.filter(key__in = ids)
            if action == 'active':
                status = True
            else:
                status = False
            #record_ids
            for record in records:
                record.isRevoked = status
                record.save()
                
            #message
            if(action == 'active'):
                messages.success(request,"Selected records has been successfully actived.")
            elif action == 'inactive':
                messages.success(request,"Selected records has been successfully inactived.")
            else:
                messages.success(request,"Selected records has been successfully verified.")

            return redirect(str(settings.SITE_URL)+'/backend/apikey/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/apikey/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#generate api key
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def apikey_generate(request):
    try:
        api_key                = APIAuthKey()
        api_key.ipaddress      = request.META['REMOTE_ADDR']
        api_key.browserAgent   = request.META['HTTP_USER_AGENT']
        api_key.createdBy      = request.user
        api_key.save()

        messages.success(request,"API Access Key has been successfully generated.")
        return redirect(str(settings.SITE_URL)+'/backend/apikey/listing')
    except Exception as e:
        db_logger.exception(e)
        return e