from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http.response import  HttpResponseRedirect
from django.contrib import messages
from django.views.decorators.cache  import cache_control
from accountapp.models import *
from blogapp.models import *
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

#blog listing
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_list(request, template_name='backend/blog/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'blog-search-post' in request.session:
                    del request.session['blog-search-post']
                return redirect(str(settings.SITE_URL)+'/backend/blog/listing')
            else:
                request.session['blog-search-post']     = request.POST
                Post_Data                               = request.POST
        else:
            if 'blog-search-post' in request.session:
                Post_Data = request.session['blog-search-post']
            else:
                Post_Data = []

        #check session
        if Post_Data:
            form = BlogListFilter(Post_Data)
        else:
            form = BlogListFilter()

        complexQuery   = Q()

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            if search:
                complexQuery.add(Q(title__icontains=search), complexQuery.AND)
        objs        = Blog.objects.filter(complexQuery).order_by('-id')
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

#blog status
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_status(request):
    try:
        #get post
        if request.method == 'POST':
            action  = request.POST['action_on']
            ids     = request.POST.getlist('records')
            records = Blog.objects.filter(token__in = ids)
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

            return redirect(str(settings.SITE_URL)+'/backend/blog/listing')
        else:    
            return redirect(str(settings.SITE_URL)+'/backend/blog/listing')
    except Exception as e:
            db_logger.exception(e)
            return e

#blog view
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_view(request, token, template_name='backend/blog/detail.html'):
    try:
        blog  = get_object_or_404(Blog, token=token)
        return render(request, template_name, {'object':blog})
    except Exception as e:
        db_logger.exception(e)
        return e
#blog create
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_create(request, template_name='backend/blog/add.html'):
    try:
        if request.method == 'POST':
            form = BlogCreateForm(request.POST, request.FILES)
            if form.is_valid():
                blog = form.save()
                blog.ipaddress      = request.META['REMOTE_ADDR']
                blog.browserinfo    = request.META['HTTP_USER_AGENT']
                blog.createdBy      = request.user
                blog.save()
                messages.success(request,"Blog has been successfully added.")
                return redirect(str(settings.SITE_URL)+'/backend/blog/listing')
        else:
            form = BlogCreateForm(request.POST or None)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#blog update
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_update(request, token, template_name='backend/blog/edit.html'):
    try:
        blog = get_object_or_404(Blog, token=token)
        if request.method == 'POST':
            form = BlogCreateForm(request.POST, request.FILES, instance=blog)
            if form.is_valid():
                form.save()
                messages.success(request,"Blog has been successfully updated.")
                return redirect(str(settings.SITE_URL)+'/backend/blog/listing')
        else:
            form  = BlogCreateForm(request.POST or None, instance=blog)
        return render(request, template_name, {'form':form})
    except Exception as e:
            db_logger.exception(e)
            return e

#blog delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_delete(request, token, template_name='backend/blog/confirm_delete.html'):
    try:
        blog = get_object_or_404(Blog, token=token)
        if request.method=='POST':
            blog.delete()
            messages.success(request,"Blog has been successfully deleted.")
            return redirect(str(settings.SITE_URL)+'/backend/blog/listing')
        return render(request, template_name, {'object':blog})
    except Exception as e:
            db_logger.exception(e)
            return e

#blog delete
@login_required(login_url=str(settings.SITE_URL)+'/backend/login') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_comment_delete(request, token, pk):
    try:
        blogcomment = get_object_or_404(BlogComment, pk=pk)
        blogcomment.delete()
        messages.success(request,"Comment has been successfully deleted.")
        return redirect(str(settings.SITE_URL)+'/backend/blog/view/'+str(token))
    except Exception as e:
            db_logger.exception(e)
            return e