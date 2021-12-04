from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import  HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.cache  import cache_control
from accountapp.models import *
from jobapp.models import *
from backendapp.forms import *
from backendapp.latlong import *
from backendapp.decorator import check_role_permission
from django.contrib.auth.models import Group
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import resolve
import logging
db_logger = logging.getLogger('backendapp')

#job listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_list(request, template_name='backend/job/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'job-search-post' in request.session:
                    del request.session['job-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/job/listing')
            else:
                request.session['job-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'job-search-post' in request.session:
                Post_Data = request.session['job-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = JobListFilter(Post_Data)
        else:
            form = JobListFilter()

        complexQuery   = Q()

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            if search:
                complexQuery.add(Q(title__icontains=search) | Q(hiring_manager_name__icontains=search) | Q(hiring_company__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search), complexQuery.AND)
        objs        = Job.objects.filter(complexQuery).order_by('-id')
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

#job status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            records = Job.objects.filter(token__in = ids)
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

            return redirect(str(settings.SITE_URL)+'/backend/job/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/job/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#job view
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_view(request, token, template_name='backend/job/detail.html'):
    try:
        job             = get_object_or_404(Job, token=token)
        no_of_pending   = JobOffer.objects.filter(job=job, action='Pending').order_by('-id')
        no_of_accept    = JobOffer.objects.filter(job=job, action='Accept').order_by('-updatedAt')
        no_of_decline   = JobOffer.objects.filter(job=job, action='Decline').order_by('-updatedAt')
        schedule        = JobShiftSchedule.objects.filter(job=job).first()

        return render(request, template_name, {'object':job, 'no_of_pending':no_of_pending, 'no_of_accept':no_of_accept, 'no_of_decline':no_of_decline, 'schedule':schedule})
    except Exception as e:
            db_logger.exception(e)
            return e
#job create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_create(request, template_name='backend/job/add.html'):
    try:
        if request.method == 'POST':
            form = JobCreateForm(request.POST, request.FILES)
            if form.is_valid():
                job = form.save()
                job.ipaddress      = request.META['REMOTE_ADDR']
                job.browserinfo    = request.META['HTTP_USER_AGENT']
                job.createdBy      = request.user
                subscription    = Subscription.objects.filter(user=job.user,status='Current').first()
                if subscription is None:
                    subscription     = Subscription.objects.filter(user=job.user).last()
                if subscription:
                    job.subscription = subscription
                job.save()
                #find latlong
                address     = str(job.address)+','+str(job.city.name)+','+str(job.zipcode)+' '+str(job.state.code)+',USA'
                response    = find_LatLong(address)
                if response['status'] == 'OK':
                    result         = response['results'][0]
                    job.latitude   = result['geometry']['location']['lat']
                    job.longitude  = result['geometry']['location']['lng']
                    job.save()
                messages.success(request,"Job has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/job/listing')
        else:
            form = JobCreateForm(request.POST or None)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#job update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_update(request, token, template_name='backend/job/edit.html'):
    try:
        job = get_object_or_404(Job, token=token)
        if request.method == 'POST':
            form = JobCreateForm(request.POST, request.FILES, instance=job)
            if form.is_valid():
                job = form.save()
                #find latlong
                address     = str(job.address)+','+str(job.city.name)+','+str(job.zipcode)+' '+str(job.state.code)+',USA'
                response    = find_LatLong(address)
                if response['status'] == 'OK':
                    result         = response['results'][0]
                    job.latitude   = result['geometry']['location']['lat']
                    job.longitude  = result['geometry']['location']['lng']
                    job.save()
                messages.success(request,"Job has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/backend/job/listing')
        else:
            form  = JobCreateForm(request.POST or None, instance=job)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#job delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_delete(request, token, template_name='backend/job/confirm_delete.html'):
    try:
        job = get_object_or_404(Job, token=token)
        if request.method=='POST':
            job.delete()
            messages.success(request,"Job has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/job/listing')
        return render(request, template_name, {'object':job})
    except Exception as e:
            db_logger.exception(e)
            return e

#jobseeker listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_list(request, token, template_name='backend/job/jobseeker.html'):
    try:
        job = get_object_or_404(Job, token=token)
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'job-jobseeker-search-post' in request.session:
                    del request.session['job-jobseeker-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/job/jobseeker/'+str(token))
            else:
                request.session['job-jobseeker-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'job-jobseeker-search-post' in request.session:
                Post_Data = request.session['job-jobseeker-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = JobJobseekerListFilter(Post_Data)
        else:
            form = JobJobseekerListFilter()

        complexQuery   = Q(is_staff=False, is_superuser=False, groups__name='Jobseeker', is_active=True)

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            available   = Post_Data['available'] if Post_Data['available'] else ''
            category    = Post_Data['category'] if Post_Data['category'] else ''
            if search:
                complexQuery.add(Q(email__icontains=search) | Q(first_name__icontains=search) | Q(last_name__icontains=search) | Q(company__icontains=search) | Q(mobile__icontains=search), complexQuery.AND)
            if available:
                complexQuery.add(Q(available=available), complexQuery.AND)
            if category:
                complexQuery.add(Q(usercategory__category_id=category), complexQuery.AND)
            users       = User.objects.filter(complexQuery).order_by('-id')
            if users:
                for user in users:
                    offer = JobOffer.objects.filter(user=user, job=job).first()
                    if offer:
                        user.offer          = 'Yes'
                        user.offer_action   = offer.action
                    else:
                        user.offer          = 'No'
                        user.offer_action   = ''

            paginator   = Paginator(users, settings.PER_PAGE_RECORD)
            page        = request.GET.get('page')
            records     = paginator.get_page(page)
            
        else:
            records     = []
        data = {}
        data['object_list'] = records
        data['form']        = form
        data['job']         = job
        return render(request, template_name, data)
    except Exception as e:
            db_logger.exception(e)
            return e

#job jobseeker send request
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobseeker_send_request(request, token):
    try:
        job             = get_object_or_404(Job, token=token)
        subscription    = Subscription.objects.filter(user=job.user,status='Current').first()
        if subscription is None:
            subscription    = Subscription.objects.filter(user=job.user).last()
        #get post
        if request.method == 'POST':
            ids     = request.POST.getlist('records')
            records = User.objects.filter(token__in = ids)
            for record in records:
                offer               = JobOffer()
                offer.user          = record
                offer.job           = job
                if subscription:
                    offer.subscription = subscription
                offer.ipaddress     = request.META['REMOTE_ADDR']
                offer.browserinfo   = request.META['HTTP_USER_AGENT']
                offer.createdBy     = request.user
                offer.save()
            messages.success(request,"Request has been sent successfully.")
            return redirect(str(settings.SITE_URL)+'/backend/job/jobseeker/'+str(token))
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/job/jobseeker/'+str(token))
    except Exception as e:
            db_logger.exception(e)
            return e

#user change update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_schedule(request, token, template_name='backend/job/schedule.html'):
    try:
        job             = get_object_or_404(Job, token=token)
        schedule        = JobShiftSchedule.objects.filter(job=job).first()
        if request.method == 'POST': 
            if schedule:
                form = JobScheduleForm(request.POST, instance=schedule, job=job)
            else:
                form = JobScheduleForm(request.POST, job=job)
            if form.is_valid():
                sch = form.save()
                sch.ipaddress      = request.META['REMOTE_ADDR']
                sch.browserinfo    = request.META['HTTP_USER_AGENT']
                sch.createdBy      = request.user
                sch.save()
                messages.success(request,"Schedule has been successfully changed.")
                return redirect(str(settings.SITE_URL)+'/backend/job/schedule/'+str(token))
        else:
            if schedule:
                form = JobScheduleForm(request.POST or None, instance=schedule, job=job)
            else:
                form = JobScheduleForm(request.POST or None, job=job)
        return render(request, template_name, {'form':form})
    except Exception as e:
        db_logger.exception(e)
        return e