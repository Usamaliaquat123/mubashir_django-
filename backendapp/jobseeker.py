from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import  HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.cache  import cache_control
from accountapp.models import *
from backendapp.forms import *
from backendapp.decorator import check_role_permission
from backendapp.latlong import *
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import resolve
import logging
db_logger = logging.getLogger('backendapp')

#jobseeker listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_list(request, template_name='backend/jobseeker/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'jobseeker-search-post' in request.session:
                    del request.session['jobseeker-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/jobseeker/listing')
            else:
                request.session['jobseeker-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'jobseeker-search-post' in request.session:
                Post_Data = request.session['jobseeker-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = JobseekerListFilter(Post_Data)
        else:
            form = JobseekerListFilter()

        complexQuery   = Q(is_staff=False, is_superuser=False, groups__name='Jobseeker')

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            is_active   = Post_Data['is_active'] if Post_Data['is_active'] else ''
            available   = Post_Data['available'] if Post_Data['available'] else ''
            if search:
                complexQuery.add(Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(company__icontains=search) | Q(mobile__icontains=search), complexQuery.AND)
            if is_active:
                complexQuery.add(Q(is_active=is_active), complexQuery.AND)
            if available:
                complexQuery.add(Q(available=available), complexQuery.AND)
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

#jobseeker status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            users   = User.objects.filter(groups__name='Jobseeker', token__in = ids)
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

            return redirect(str(settings.SITE_URL)+'/backend/jobseeker/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/jobseeker/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#jobseeker view
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_view(request, token, template_name='backend/jobseeker/detail.html'):
    try:
        user        = get_object_or_404(User, groups__name='Jobseeker', is_staff=False, token=token)
        schedule    = Schedule.objects.filter(user=user, status='Current').first()
        offers      = JobOffer.objects.filter(user=user).order_by('-id')
        return render(request, template_name, {'object':user, 'schedule' : schedule, 'offers' : offers})
    except Exception as e:
            db_logger.exception(e)
            return e

#jobseeker create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_create(request, template_name='backend/jobseeker/add.html'):
    try:
        categories = Category.objects.filter(publish=True).order_by('name')
        for category in categories:
            subcategories = Subcategory.objects.filter(category=category).order_by('name')
            category.subcategories = subcategories

        if request.method == 'POST':
            form = JobseekerCreateForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save()
                user.set_password(request.POST['password1'])
                #save user group
                group = Group.objects.get(name='Jobseeker')
                user.groups.add(group)
                #save user group
                user.ipaddress      = request.META['REMOTE_ADDR']
                user.browserinfo    = request.META['HTTP_USER_AGENT']
                user.createdBy      = request.user
                user.save()
                #category
                categories = request.POST.getlist('category')
                if categories:
                    for category in categories:
                        uc              = UserCategory()
                        uc.user         = user
                        uc.category     = get_object_or_404(Category, token=category)
                        uc.save()
                        subcategories   = request.POST.getlist('sub_'+str(category))
                        if subcategories:
                            subcategory  = Subcategory.objects.filter(token__in=subcategories)
                            if subcategory:
                                uc.subcategory.set(subcategory)
                                uc.save()
                
                #find latlong
                address     = str(user.address)+','+str(user.city.name)+','+str(user.zipcode)+' '+str(user.state.code)+',USA'
                response    = find_LatLong(address)
                if response['status'] == 'OK':
                    result         = response['results'][0]
                    user.latitude   = result['geometry']['location']['lat']
                    user.longitude  = result['geometry']['location']['lng']
                    user.save()

                messages.success(request,"Jobseeker has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/jobseeker/listing')
        else:

            form = JobseekerCreateForm(request.POST or None)
            
        return render(request, template_name, {'form':form, 'categories' : categories})
    except Exception as e:
            db_logger.exception(e)
            return e

#jobseeker update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_update(request, token, template_name='backend/jobseeker/edit.html'):
    try:
        user = get_object_or_404(User, groups__name='Jobseeker', is_staff=False, token=token)
        categories = Category.objects.filter(publish=True).order_by('name')
        for category in categories:
                selected = UserCategory.objects.filter(user=user, category = category).first()
                if selected:
                    category.selected = 'Yes'
                else:
                    category.selected = 'No'
                subcategories = Subcategory.objects.filter(category=category).order_by('name')
                for sub in subcategories:
                    subselected = 'No'
                    if selected:
                        subselected = UserCategory.objects.filter(user=user, category = category, subcategory__id = sub.id).first()
                        if subselected:
                            subselected = 'Yes'
                        else:
                            subselected = 'No'
                    sub.selected = subselected
                category.subcategories = subcategories
        
        if request.method == 'POST':
            form = JobseekerUpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                user = form.save()
                #delete old categories
                UserCategory.objects.filter(user=user).delete()
                #category
                categories = request.POST.getlist('category')
                if categories:
                    for category in categories:
                        uc              = UserCategory()
                        uc.user         = user
                        uc.category     = get_object_or_404(Category, token=category)
                        uc.save()
                        subcategories   = request.POST.getlist('sub_'+str(category))
                        if subcategories:
                            subcategory  = Subcategory.objects.filter(token__in=subcategories)
                            if subcategory:
                                uc.subcategory.set(subcategory)
                                uc.save()
                
                #find latlong
                address     = str(user.address)+','+str(user.city.name)+','+str(user.zipcode)+' '+str(user.state.code)+',USA'
                response    = find_LatLong(address)
                if response['status'] == 'OK':
                    result         = response['results'][0]
                    user.latitude   = result['geometry']['location']['lat']
                    user.longitude  = result['geometry']['location']['lng']
                    user.save()

                messages.success(request,"Jobseeker has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/backend/jobseeker/listing')
        else:
            form  = JobseekerUpdateForm(request.POST or None, instance=user)

        return render(request, template_name, {'form':form, 'categories' : categories})
    except Exception as e:
            db_logger.exception(e)
            return e

#jobseeker delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_delete(request, token, template_name='backend/jobseeker/confirm_delete.html'):
    try:
        user = get_object_or_404(User, groups__name='Jobseeker', is_staff=False, token=token)
        if request.method=='POST':
            user.delete()
            messages.success(request,"jobseeker has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/jobseeker/listing')
        return render(request, template_name, {'object':user})
    except Exception as e:
            db_logger.exception(e)
            return e

#user change update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_change_password(request, token, template_name='backend/jobseeker/change-password.html'):
    user = get_object_or_404(User, groups__name='Jobseeker', is_staff=False, token=token)
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            user.set_password(request.POST['password1'])
            user.save()
            messages.success(request,"Password has been successfully changed.")
            return redirect(str(settings.SITE_URL)+'/backend/jobseeker/listing')
    else:
        form = ChangePasswordForm(request.POST or None, instance=user)
    return render(request, template_name, {'form':form})

#jobseeker shcedule
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_schedule(request, token, template_name='backend/jobseeker/schedule.html'):
    user = get_object_or_404(User, groups__name='Jobseeker', is_staff=False, token=token)
    schedule = Schedule.objects.filter(user=user, status='Current').first()
    if request.method == 'POST':
        if schedule:
            form = JobseekerScheduleForm(request.POST, instance=schedule, user=user)
        else:
            form = JobseekerScheduleForm(request.POST, user=user)
        if form.is_valid():
            sch = form.save()
            sch.ipaddress      = request.META['REMOTE_ADDR']
            sch.browserinfo    = request.META['HTTP_USER_AGENT']
            sch.createdBy      = request.user
            sch.save()
            messages.success(request,"Schedule has been successfully changed.")
            return redirect(str(settings.SITE_URL)+'/backend/jobseeker/listing')
    else:
        if schedule:
            form = JobseekerScheduleForm(request.POST or None, instance=schedule, user=user)
        else:
            form = JobseekerScheduleForm(request.POST or None, user=user)

    return render(request, template_name, {'form':form})
