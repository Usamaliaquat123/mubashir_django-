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

#subscription listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_list(request, template_name='backend/subscription/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'subscription-search-post' in request.session:
                    del request.session['subscription-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/subscription/listing')
            else:
                request.session['subscription-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'subscription-search-post' in request.session:
                Post_Data = request.session['subscription-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = SubscriptionListFilter(Post_Data)
        else:
            form = SubscriptionListFilter()

        complexQuery   = Q()

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            active      = Post_Data['active'] if Post_Data['active'] else ''
            plan        = Post_Data['plan'] if Post_Data['plan'] else ''
            if search:
                complexQuery.add(Q(name__icontains=search), complexQuery.AND)
            if plan:
                complexQuery.add(Q(plan=plan), complexQuery.AND)
            if active:
                complexQuery.add(Q(active=active), complexQuery.AND)
        
        objs        = Subscription.objects.filter(complexQuery).order_by('-id')
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

#subscription status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            records = Subscription.objects.filter(token__in = ids)
            if action == 'active':
                status = True
            elif action == 'inactive':
                status = False
            else:
                status = True
            #record_ids
            for record in records:
                record.active = status
                record.save() 
                
            #message
            if(action == 'active'):
                messages.success(request,"Selected records has been successfully actived.")
            elif action == 'inactive':
                messages.success(request,"Selected records has been successfully inactived.")
            else:
                messages.success(request,"Selected records has been successfully verified.")

            return redirect(str(settings.SITE_URL)+'/backend/subscription/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/subscription/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#subscription create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_create(request, template_name='backend/subscription/add.html'):
    try:
        if request.method == 'POST':
            form = SubscriptionCreateForm(request.POST)
            if form.is_valid():

                #change old subscription status
                old_subscription = Subscription.objects.filter(user=request.POST['user'],status='Current').first()
                if old_subscription:
                    old_subscription.status = 'Old'
                    old_subscription.save()
                
                #get plan information
                plan = Plan.objects.filter(id=request.POST['plan']).first()

                #save new subscription data
                subscription = form.save()
                subscription.ipaddress      = request.META['REMOTE_ADDR']
                subscription.browserinfo    = request.META['HTTP_USER_AGENT']
                subscription.createdBy      = request.user
                subscription.period         = plan.period
                subscription.payment_type   = 'Offline'
                subscription.payment_status = 'Success'
                subscription.save()
                messages.success(request,"Subscription has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/subscription/listing')
        else:
            form = SubscriptionCreateForm(request.POST or None)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#subscription view
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_view(request, token, template_name='backend/subscription/detail.html'):
    try:
        obj        = get_object_or_404(Subscription,token=token)
        objects   = Subscription.objects.filter(user=obj.user).exclude(id=obj.id).order_by('-id')
        return render(request, template_name, {'object':obj,'objects':objects})
    except Exception as e:
            db_logger.exception(e)
            return e