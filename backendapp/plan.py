from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import  HttpResponseRedirect
from django.http import JsonResponse
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
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
db_logger = logging.getLogger('backendapp')

#plan listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def plan_list(request, template_name='backend/plan/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'plan-search-post' in request.session:
                    del request.session['plan-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/plan/listing')
            else:
                request.session['plan-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'plan-search-post' in request.session:
                Post_Data = request.session['plan-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = PlanListFilter(Post_Data)
        else:
            form = PlanListFilter()

        complexQuery   = Q()

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            publish   = Post_Data['publish'] if Post_Data['publish'] else ''
            if search:
                complexQuery.add(Q(name__icontains=search), complexQuery.AND)
            if publish:
                complexQuery.add(Q(publish=publish), complexQuery.AND)
        
        objs        = Plan.objects.filter(complexQuery).order_by('name')
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

#plan status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def plan_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            records = Plan.objects.filter(token__in = ids)
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

            return redirect(str(settings.SITE_URL)+'/backend/plan/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/plan/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#plan create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def plan_create(request, template_name='backend/plan/add.html'):
    try:
        if request.method == 'POST':
            form = PlanForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Plan has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/plan/listing')
        else:
            form = PlanForm(request.POST or None)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#plan update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def plan_update(request, token, template_name='backend/plan/edit.html'):
    try:
        plan = get_object_or_404(Plan, token=token)
        if request.method == 'POST':
            form = PlanForm(request.POST, instance=plan)
            if form.is_valid():
                form.save()
                messages.success(request,"Plan has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/backend/plan/listing')
        else:
            form  = PlanForm(request.POST or None, instance=plan)

        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#plan delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def plan_delete(request, token, template_name='backend/plan/confirm_delete.html'):
    try:
        plan = get_object_or_404(Plan, token=token)
        if request.method=='POST':
            plan.delete()
            messages.success(request,"Plan has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/plan/listing')
        return render(request, template_name, {'object':plan})
    except Exception as e:
            db_logger.exception(e)
            return e

#plan details
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def plan_detail(request, token):
    try:
        plan        = get_object_or_404(Plan, pk=token)
        startdate   = datetime.now()
        if plan.period == 'yearly':
            enddate     = startdate + relativedelta(months=+12)
        elif plan.period == 'half-yearly':
            enddate     = startdate + relativedelta(months=+6)
        elif plan.period == 'quarterly':
            enddate     = startdate + relativedelta(months=+3)
        else:
            enddate     = startdate + relativedelta(months=+1)
        
        startdate   = startdate.strftime('%Y-%m-%d')
        enddate     = enddate.strftime('%Y-%m-%d')

        return JsonResponse({'amount':plan.amount,'startdate':startdate,'enddate':enddate})
    except Exception as e:
            db_logger.exception(e)
            return e