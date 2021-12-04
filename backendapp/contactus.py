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

#contactus listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contactus_list(request, template_name='backend/contactus/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'contactus-search-post' in request.session:
                    del request.session['contactus-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/contactus/listing')
            else:
                request.session['contactus-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'contactus-search-post' in request.session:
                Post_Data = request.session['contactus-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = ContactUsListFilter(Post_Data)
        else:
            form = ContactUsListFilter()

        complexQuery   = Q()

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            if search:
                complexQuery.add(Q(name__icontains=search) | Q(email__icontains=search) | Q(phone__icontains=search) | Q(message__icontains=search), complexQuery.AND)
        objs        = ContactUs.objects.filter(complexQuery).order_by('-id')
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

#contactus view
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contactus_view(request, pk, template_name='backend/contactus/detail.html'):
    try:
        obj  = get_object_or_404(ContactUs, pk=pk)
        return render(request, template_name, {'object':obj})
    except Exception as e:
        db_logger.exception(e)
        return e
#contactus delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contactus_delete(request, pk, template_name='backend/contactus/confirm_delete.html'):
    try:
        obj = get_object_or_404(ContactUs, pk=pk)
        if request.method=='POST':
            obj.delete()
            messages.success(request,"Contact Us has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/contactus/listing')
        return render(request, template_name, {'object':obj})
    except Exception as e:
            db_logger.exception(e)
            return e