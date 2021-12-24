from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import  HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.cache  import cache_control
from accountapp.models import *
from backendapp.forms import *
from backendapp.decorator import check_role_permission
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import resolve
import logging
db_logger = logging.getLogger('backendapp')

#city listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def city_list(request, template_name='backend/city/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'city-search-post' in request.session:
                    del request.session['city-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/city/listing')
            else:
                request.session['city-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'city-search-post' in request.session:
                Post_Data = request.session['city-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = CityListFilter(Post_Data)
        else:
            form = CityListFilter()

        complexQuery   = Q()

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            publish     = Post_Data['publish'] if Post_Data['publish'] else ''
            state       = Post_Data['state'] if Post_Data['state'] else ''
            if search:
                complexQuery.add(Q(name__icontains=search), complexQuery.AND)
            if publish:
                complexQuery.add(Q(publish=publish), complexQuery.AND)
            if state:
                complexQuery.add(Q(state=state), complexQuery.AND)
        
        objs        = City.objects.filter(complexQuery).order_by('name')
        paginator   = Paginator(objs, settings.PER_PAGE_RECORD)
        page        = request.GET.get('page')
        records     = paginator.get_page(page)
        data = {}
        data['object_list'] = records
        data['form']        = form
        return render(request, template_name, data)
    except Exception as e:
            db_logger.exception(e)
            return e

#city status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def city_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            records = City.objects.filter(token__in = ids)
            if action == 'active':
                status = True
            elif action == 'inactive':
                status = False
            else:
                status = True
            #record_ids
            for record in records:
                record.publish = status
                record.save()
                
            #message
            if(action == 'active'):
                messages.success(request,"Selected records has been successfully actived.")
            elif action == 'inactive':
                messages.success(request,"Selected records has been successfully inactived.")
            else:
                messages.success(request,"Selected records has been successfully verified.")

            return redirect(str(settings.SITE_URL)+'/backend/city/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/city/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#city create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def city_create(request, template_name='backend/city/add.html'):
    try:
        if request.method == 'POST':
            form = CityForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"City has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/city/listing')
        else:
            form = CityForm(request.POST or None)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#city update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def city_update(request, token, template_name='backend/city/edit.html'):
    try:
        city = get_object_or_404(City, token=token)
        if request.method == 'POST':
            form = CityForm(request.POST, instance=city)
            if form.is_valid():
                form.save()
                messages.success(request,"City has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/backend/city/listing')
        else:
            form  = CityForm(request.POST or None, instance=city)

        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#city delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def city_delete(request, token, template_name='backend/city/confirm_delete.html'):
    try:
        city = get_object_or_404(City, token=token)
        if request.method=='POST':
            city.delete()
            messages.success(request,"City has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/city/listing')
        return render(request, template_name, {'object':city})
    except Exception as e:
            db_logger.exception(e)
            return e