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

#language listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def language_list(request, template_name='backend/language/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'language-search-post' in request.session:
                    del request.session['language-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/language/listing')
            else:
                request.session['language-search-post']     = request.POST
                Post_Data                                   = request.POST
        else:
            if 'language-search-post' in request.session:
                Post_Data = request.session['language-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = LanguageListFilter(Post_Data)
        else:
            form = LanguageListFilter()

        complexQuery   = Q()

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            publish   = Post_Data['publish'] if Post_Data['publish'] else ''
            if search:
                complexQuery.add(Q(name__icontains=search), complexQuery.AND)
            if publish:
                complexQuery.add(Q(publish=publish), complexQuery.AND)
        
        objs        = Language.objects.filter(complexQuery).order_by('name')
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

#language status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def language_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            records = Language.objects.filter(token__in = ids)
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

            return redirect(str(settings.SITE_URL)+'/backend/language/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/language/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#language create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def language_create(request, template_name='backend/language/add.html'):
    try:
        if request.method == 'POST':
            form = LanguageForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Language has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/language/listing')
        else:
            form = LanguageForm(request.POST or None)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#language update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def language_update(request, token, template_name='backend/language/edit.html'):
    try:
        language = get_object_or_404(Language, token=token)
        if request.method == 'POST':
            form = LanguageForm(request.POST, instance=language)
            if form.is_valid():
                form.save()
                messages.success(request,"Language has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/backend/language/listing')
        else:
            form  = LanguageForm(request.POST or None, instance=language)

        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#language delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def language_delete(request, token, template_name='backend/language/confirm_delete.html'):
    try:
        language = get_object_or_404(Language, token=token)
        if request.method=='POST':
            language.delete()
            messages.success(request,"Language has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/language/listing')
        return render(request, template_name, {'object':language})
    except Exception as e:
            db_logger.exception(e)
            return e