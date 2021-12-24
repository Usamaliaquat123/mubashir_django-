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

#state listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def state_list(request, template_name='backend/state/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'state-search-post' in request.session:
                    del request.session['state-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/state/listing')
            else:
                request.session['state-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'state-search-post' in request.session:
                Post_Data = request.session['state-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = StateListFilter(Post_Data)
        else:
            form = StateListFilter()

        complexQuery   = Q()

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            publish   = Post_Data['publish'] if Post_Data['publish'] else ''
            if search:
                complexQuery.add(Q(name__icontains=search), complexQuery.AND)
            if publish:
                complexQuery.add(Q(publish=publish), complexQuery.AND)
        
        objs        = State.objects.filter(complexQuery).order_by('name')
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

#state status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def state_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            records = State.objects.filter(token__in = ids)
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

            return redirect(str(settings.SITE_URL)+'/backend/state/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/state/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#state create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def state_create(request, template_name='backend/state/add.html'):
    try:
        if request.method == 'POST':
            form = StateForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"State has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/state/listing')
        else:
            form = StateForm(request.POST or None)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#state update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def state_update(request, token, template_name='backend/state/edit.html'):
    try:
        state = get_object_or_404(State, token=token)
        if request.method == 'POST':
            form = StateForm(request.POST, instance=state)
            if form.is_valid():
                form.save()
                messages.success(request,"State has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/backend/state/listing')
        else:
            form  = StateForm(request.POST or None, instance=state)

        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#state delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def state_delete(request, token, template_name='backend/state/confirm_delete.html'):
    try:
        state = get_object_or_404(State, token=token)
        if request.method=='POST':
            state.delete()
            messages.success(request,"State has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/state/listing')
        return render(request, template_name, {'object':state})
    except Exception as e:
            db_logger.exception(e)
            return e