from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import *
from accountapp.models import *
from jobapp.models import *
from backendapp.decorator import check_role_permission
from django.http.response import  HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.cache  import cache_control
import logging
from datetime import date, timedelta
from django.db.models import Count
from django.conf import settings
import json
db_logger = logging.getLogger('backendapp')

#backend login view
def login_view(request):
    try:
        #already login user
        if request.user.is_authenticated:
                return redirect(str(settings.SITE_URL)+'/backend/dashboard')
        #check post login user
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                info = User.objects.filter(email = username, groups__name='Admin').first()
                user = authenticate(email=info.email, password=password)
                if user is not None:
                    login(request, user)
                    db_logger.info(str(username)+" is successfully login in Backend")
                    return redirect(str(settings.SITE_URL)+'/backend/dashboard')
                else:
                    db_logger.warning(str(username)+" is not found")
                    messages.error(request, str(username)+" is not found")
                    return redirect(str(settings.SITE_URL)+'/backend/login')
        else:
            form = LoginForm()
        
        context = {"form": form,}
        return render(request, 'backend/login.html', context)

    except Exception as e:
            db_logger.exception(e)
            return e

#backend logout page
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_view(request):
    try:
        username = request.user.email
        logout(request)
        db_logger.info(str(username)+" is successfully logout from Backend")
        return HttpResponseRedirect(str(settings.SITE_URL)+'/backend/login')
    except Exception as e:
            db_logger.exception(e)
            return e

#backend Dashboard
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    try:
        context         = {}
        context['total_emp']       = User.objects.filter(groups__name='Employer').count()
        context['employers']       = User.objects.filter(groups__name='Employer').order_by('-id')[:5]
        context['Jobseekers']      = User.objects.filter(groups__name='Jobseeker').order_by('-id')[:5]
        context['total_subs']      = Subscription.objects.all().count()
        context['total_js']        = User.objects.filter(groups__name='Jobseeker').count()
        context['jobs']            = Job.objects.all().order_by('-id')[:10]
        context['total_jobs']      = Job.objects.all().count()
        context['total_offers']    = JobOffer.objects.all().count()
        context['accept_offers']   = JobOffer.objects.filter(action='Accept').order_by('-id')[:10]
        context['decline_offers']  = JobOffer.objects.filter(action='Decline').order_by('-id')[:10]
        context['pending_offers']  = JobOffer.objects.filter(action='Pending').order_by('-id')[:10]
        today                      = date.today()
        last_week_dates            = [today - timedelta(6), today - timedelta(5), today - timedelta(4), today - timedelta(3), today - timedelta(2), today - timedelta(1), today]
        dates_label = []
        emp_count   = []
        js_count    = []
        for lwd in last_week_dates:
            date_formate = str(lwd.strftime("%d %b"))
            dates_label.append(date_formate)
            emp_count.append(User.objects.filter(groups__name='Employer', date_joined__date = lwd).count())
            js_count.append(User.objects.filter(groups__name='Jobseeker', date_joined__date = lwd).count())
        context['last_week_dates']          = json.dumps(dates_label)
        context['last_week_employers']      = json.dumps(emp_count)
        context['last_week_jobseekers']     = json.dumps(js_count)
        return render(request, 'backend/dashboard.html', context)
    except Exception as e:
        db_logger.exception(e)
        return e

#profile
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    try:
        #check post user
        if request.method == 'POST':
            form = ProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile has been updated successfully!')
                return redirect(str(settings.SITE_URL)+'/backend/profile')
        else:
            form = ProfileForm(request.POST or None, instance=request.user)
        
        context = {"form": form,}
        return render(request, 'backend/profile.html', context)

    except Exception as e:
            db_logger.exception(e)
            return e

#change password
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def change_password(request):
    try:
        #check post user
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password has been changed successfully!')
                return redirect(str(settings.SITE_URL)+'/backend/change-password')
        else:
            form = PasswordChangeForm(request.user)
        
        context = {"form": form,}
        return render(request, 'backend/change-password.html', context)

    except Exception as e:
            db_logger.exception(e)
            return e

#cities
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def cities(request, pk):
    try:
        options         = '<option value="" selected="">Select City</option>'
        cities_list     = City.objects.filter(state_id=pk, publish=True).order_by('name') 
        if cities_list:
            for city in cities_list:
                options += '<option value="'+str(city.id)+'">'+str(city.name)+'</option>'
        return HttpResponse(options)
    except Exception as e:
            db_logger.exception(e)
            return e

#subcategories
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subcategories(request, pk):
    try:
        options         = ''
        sub_list     = Subcategory.objects.filter(category_id=pk, publish=True).order_by('name') 
        if sub_list:
            for sub in sub_list:
                options += '<option value="'+str(sub.id)+'">'+str(sub.name)+'</option>'
        return HttpResponse(options)
    except Exception as e:
            db_logger.exception(e)
            return e
