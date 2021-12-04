from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import  HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.cache  import cache_control
from accountapp.models import *
from backendapp.forms import *
from backendapp.decorator import check_role_permission
from jobapp.models import *
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import resolve
import logging
db_logger = logging.getLogger('backendapp')

#employer listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def employer_list(request, template_name='backend/employer/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'employer-search-post' in request.session:
                    del request.session['employer-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/employer/listing')
            else:
                request.session['employer-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'employer-search-post' in request.session:
                Post_Data = request.session['employer-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = EmployerListFilter(Post_Data)
        else:
            form = EmployerListFilter()

        complexQuery   = Q(is_staff=False, is_superuser=False, groups__name='Employer')

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            is_active   = Post_Data['is_active'] if Post_Data['is_active'] else ''
            if search:
                complexQuery.add(Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(company__icontains=search) | Q(mobile__icontains=search), complexQuery.AND)
            if is_active:
                complexQuery.add(Q(is_active=is_active), complexQuery.AND)
        users       = User.objects.filter(complexQuery).order_by('-id')
        paginator   = Paginator(users, settings.PER_PAGE_RECORD)
        page        = request.GET.get('page')
        records     = paginator.get_page(page)
        data = {}
        data['object_list'] = records
        data['form']        = form
        return render(request, template_name, data)
    except Exception as e:
            db_logger.exception(e)
            return e

#employer status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def employer_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            users   = User.objects.filter(groups__name='Employer', token__in = ids)
            if action == 'active':
                status = True
            elif action == 'inactive':
                status = False
            else:
                status = True
            #record_ids
            for user in users:
                user.is_active = status
                user.save()
                
            #message
            if(action == 'active'):
                messages.success(request,"Selected records has been successfully actived.")
            elif action == 'inactive':
                messages.success(request,"Selected records has been successfully inactived.")
            else:
                messages.success(request,"Selected records has been successfully verified.")

            return redirect(str(settings.SITE_URL)+'/backend/employer/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/employer/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#employer view
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def employer_view(request, token, template_name='backend/employer/detail.html'):
    try:
        user            = get_object_or_404(User, groups__name='Employer', is_staff=False, token=token)
        jobs            = Job.objects.filter(user=user).order_by('-id')
        subscriptions   = Subscription.objects.filter(user=user).order_by('-id')
        return render(request, template_name, {'object':user, 'jobs':jobs, 'subscriptions':subscriptions})
    except Exception as e:
            db_logger.exception(e)
            return e

#employer create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def employer_create(request, template_name='backend/employer/add.html'):
    try:
        if request.method == 'POST':
            form = EmployerCreateForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                user.set_password(request.POST['password1'])
                #save user group
                group = Group.objects.get(name='Employer')
                user.groups.add(group)
                #save user group
                user.ipaddress      = request.META['REMOTE_ADDR']
                user.browserinfo    = request.META['HTTP_USER_AGENT']
                user.createdBy      = request.user
                user.save()
                messages.success(request,"Employer has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/employer/listing')
        else:

            form = EmployerCreateForm(request.POST or None)
            
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#employer update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def employer_update(request, token, template_name='backend/employer/edit.html'):
    try:
        user = get_object_or_404(User, groups__name='Employer', is_staff=False, token=token)
        if request.method == 'POST':
            form = EmployerUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                messages.success(request,"Employer has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/backend/employer/listing')
        else:
            form  = EmployerUpdateForm(request.POST or None, instance=user)

        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#employer delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def employer_delete(request, token, template_name='backend/employer/confirm_delete.html'):
    try:
        user = get_object_or_404(User, groups__name='Employer', is_staff=False, token=token)
        if request.method=='POST':
            user.delete()
            messages.success(request,"Employer has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/employer/listing')
        return render(request, template_name, {'object':user})
    except Exception as e:
            db_logger.exception(e)
            return e

#user change update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def employer_change_password(request, token, template_name='backend/employer/change-password.html'):
    user = get_object_or_404(User, groups__name='Employer', is_staff=False, token=token)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password1'])
            user.save()
            messages.success(request,"Password has been successfully changed.")
            return redirect(str(settings.SITE_URL)+'/backend/employer/listing')
    else:
        form = ChangePasswordForm(request.POST or None, instance=user)
    return render(request, template_name, {'form':form})
