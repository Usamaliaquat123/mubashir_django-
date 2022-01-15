from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from .forms import *
from accountapp.decorator import *
from accountapp.models import *
from jobapp.models import *
from backendapp.sendmail import send_reset_password_email, send_payroll_service_email
from django.http.response import  HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.cache  import cache_control
import logging
import requests
from datetime import date
from django.db.models import Count
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import resolve
db_logger = logging.getLogger('jobapp')

#job listing
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_list(request, template_name='job/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'job-search-post' in request.session:
                    del request.session['job-search-post']
                return redirect(str(settings.SITE_URL)+'/job/listing')
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

        complexQuery   = Q(user=request.user)

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            if search:
                complexQuery.add(Q(title__icontains=search) | Q(hiring_manager_name__icontains=search) | Q(hiring_company__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search), complexQuery.AND)
        objs        = Job.objects.filter(complexQuery).order_by('-id')
        if objs:
            for obj in objs:
                obj.accepted = JobOffer.objects.filter(job=obj, action='Accept').count()
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
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
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

            return redirect(str(settings.SITE_URL)+'/job/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/job/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#job view
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_view(request, token, template_name='job/detail.html'):
    try:
        job             = get_object_or_404(Job, user=request.user, token=token)
        no_of_pending   = JobOffer.objects.filter(job=job, action='Pending').order_by('-id')
        no_of_accept    = JobOffer.objects.filter(job=job, action='Accept').order_by('-updatedAt')
        no_of_decline   = JobOffer.objects.filter(job=job, action='Decline').order_by('-updatedAt')
        schedule        = JobShiftSchedule.objects.filter(job=job).first()

        return render(request, template_name, {'object':job, 'no_of_pending':no_of_pending, 'no_of_accept':no_of_accept, 'no_of_decline':no_of_decline, 'schedule':schedule})
    except Exception as e:
            db_logger.exception(e)
            return e

#job create
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_create(request, template_name='job/create.html'):
    try:
        if request.method == 'POST':
            form = JobCreateForm(request.POST, request.FILES, user=request.user)
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
                messages.success(request,"Job has been successfully created, Please set job schedule")
                return redirect(str(settings.SITE_URL)+'/job/schedule/'+str(job.token))
        else:
            form = JobCreateForm(request.POST or None, user=request.user)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#job update
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_update(request, token, template_name='job/edit.html'):
    try:
        job = get_object_or_404(Job, user=request.user, token=token)
        if request.method == 'POST':
            form = JobCreateForm(request.POST, request.FILES, instance=job, user=request.user)
            if form.is_valid():
                form.save()
                messages.success(request,"Job has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/job/listing')
        else:
            form  = JobCreateForm(request.POST or None, instance=job, user=request.user)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#job delete
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_delete(request, token, template_name='job/confirm_delete.html'):
    try:
        job = get_object_or_404(Job, user=request.user, token=token)
        if request.method=='POST':
            job.delete()
            messages.success(request,"Job has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/job/listing')
        return render(request, template_name, {'object':job})
    except Exception as e:
            db_logger.exception(e)
            return e

#job scgedule
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_schedule(request, token, template_name='job/schedule.html'):
    try:
        job             = get_object_or_404(Job, token=token)
        schedule        = JobShiftSchedule.objects.filter(job=job).first()
        isSchedule      = 'No'
        if request.method == 'POST': 
            if schedule:
                form        = JobScheduleForm(request.POST, instance=schedule, job=job)
                isSchedule  = 'Yes'
            else:
                form = JobScheduleForm(request.POST, job=job)
            if form.is_valid():
                sch = form.save()
                sch.ipaddress      = request.META['REMOTE_ADDR']
                sch.browserinfo    = request.META['HTTP_USER_AGENT']
                sch.createdBy      = request.user
                sch.save()
                messages.success(request,"Schedule has been successfully set.")
                return redirect(str(settings.SITE_URL)+'/job/listing')
        else:
            if schedule:
                form        = JobScheduleForm(request.POST or None, instance=schedule, job=job)
                isSchedule  = 'Yes'
            else:
                form = JobScheduleForm(request.POST or None, job=job)
        return render(request, template_name, {'form':form, 'isSchedule' : isSchedule})
    except Exception as e:
        db_logger.exception(e)
        return e

#job offers
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_offers(request, template_name='job/offers/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'job-search-post-offers' in request.session:
                    del request.session['job-search-post-offers']
                return redirect(str(settings.SITE_URL)+'/job/offers')
            else:
                request.session['job-search-post-offers']     = request.POST
                Post_Data                                     = request.POST
        else:
            if 'job-search-post-offers' in request.session:
                Post_Data = request.session['job-search-post-offers']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = JobOffersListFilter(Post_Data)
        else:
            form = JobOffersListFilter()

        complexQuery   = Q(job__user=request.user,action='Accept')

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            if search:
                complexQuery.add(Q(user__first_name__icontains=search) | Q(user__last_name__icontains=search) | Q(user__email__icontains=search) | Q(user__mobile__icontains=search) | Q(job__title__icontains=search) | Q(job__hiring_manager_name__icontains=search) | Q(job__hiring_company__icontains=search) | Q(job__email__icontains=search) | Q(job__phone__icontains=search), complexQuery.AND)
        objs        = JobOffer.objects.filter(complexQuery).order_by('-updatedAt')
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

#job offer update
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_offers_edit(request, token, template_name='job/offers/edit.html'):
    try:
        offer = get_object_or_404(JobOffer, job__user=request.user, token=token)
        if request.method == 'POST':
            form = JobOfferForm(request.POST, request.FILES, instance=offer)
            if form.is_valid():
                form.save()
                messages.success(request,"Job Offer has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/job/offers')
        else:
            form  = JobOfferForm(request.POST or None, instance=offer)
        return render(request, template_name, {'form':form,'object':offer})
    except Exception as e:
            db_logger.exception(e)
            return e

#job offer view
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_offers_view(request, token, template_name='job/offers/detail.html'):
    try:
        offer = get_object_or_404(JobOffer, job__user=request.user, token=token)
        return render(request, template_name, {'object':offer})
    except Exception as e:
        db_logger.exception(e)
        return e


#job offer view
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@check_subscription_permission() # - check subscription
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_offers_payroll_service(request,token):
    try:
        offer = get_object_or_404(JobOffer, job__user=request.user, token=token)
        if offer.isPayrollService:
            messages.error(request,"Already sent request for Payroll Services.")
        else:
            offer.isPayrollService = True
            offer.save()
            #send email
            send_payroll_service_email(request.user)
            messages.success(request,"Your request for Payroll Services has been sent successfully.")
        return redirect(str(settings.SITE_URL)+'/job/offers')
    except Exception as e:
        db_logger.exception(e)
        return e
