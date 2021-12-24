from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from accountapp.decorator import check_role_permission
from accountapp.models import *
from blogapp.models import *
from blogapp.forms import *
from django.http.response import  HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.cache  import cache_control
import logging
import requests
from datetime import date
from django.db.models import Count
from django.conf import settings
from django.db.models import Q
from django.core.paginator import Paginator
from django.urls import resolve
import json
from backendapp.humanizedatetime import time_ago
db_logger = logging.getLogger('jobapp')

#blog listing
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_list(request, template_name='blog/list.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'blog-search-post' in request.session:
                    del request.session['blog-search-post']
                return redirect(str(settings.SITE_URL)+'/blog')
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

        complexQuery   = Q(publish=True)
        filter_category = 'All'
        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            category    = Post_Data['category'] if Post_Data['category'] else ''
            if search:
                complexQuery.add(Q(title__icontains=search), complexQuery.AND)
            if category:
                filter_category = category
                complexQuery.add(Q(category__slug=category), complexQuery.AND)

        all_blog    = Blog.objects.filter(publish=True).count()
        objs        = Blog.objects.filter(complexQuery).order_by('-id')
        paginator   = Paginator(objs, settings.PER_PAGE_RECORD)
        page        = request.GET.get('page')
        records     = paginator.get_page(page)
        data = {}
        data['object_list']     = records
        data['form']            = form
        data['all_blog']        = all_blog
        data['filter_category'] = filter_category
        data['categories']  = BlogCategory.objects.filter(publish=True).order_by('name')
        return render(request, template_name, data)
    except Exception as e:
            db_logger.exception(e)
            return e

#blog view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_view(request, slug, template_name='blog/view.html'):
    try:
        blog            = get_object_or_404(Blog, slug=slug)
        #view by
        blogview             = BlogView()
        if request.user.is_authenticated:
            blogview.user    = request.user
        blogview.blog        = blog
        blogview.ipaddress   = request.META['REMOTE_ADDR']
        blogview.browserinfo = request.META['HTTP_USER_AGENT']
        blogview.save()

        total_comments  = BlogComment.objects.filter(blog=blog).count()
        records         = BlogComment.objects.filter(blog=blog).order_by('-id')
        paginator       = Paginator(records, settings.PER_PAGE_RECORD)
        page            = request.GET.get('page')
        comments        = paginator.get_page(page) 
        return render(request, template_name, {'object':blog,'total_comments':total_comments,'comments':comments,})
    except Exception as e:
            db_logger.exception(e)
            return e

#post comment
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_post_comment(request):
    try:
        if request.user.is_authenticated:
            blog  = get_object_or_404(Blog, pk=request.POST.get('blog'))
            comment             = BlogComment()
            comment.user        = request.user
            comment.blog        = blog
            comment.comment     = request.POST.get('comment')
            comment.ipaddress   = request.META['REMOTE_ADDR']
            comment.browserinfo = request.META['HTTP_USER_AGENT']
            comment.save()

            total_comments  = BlogComment.objects.filter(blog=blog).count()
            records         = BlogComment.objects.filter(blog=blog).order_by('-id')
            paginator       = Paginator(records, settings.PER_PAGE_RECORD)
            page            = request.GET.get('page')
            comments        = paginator.get_page(page) 

            html = ''
            for comment in comments:
                createdAt = time_ago(comment.createdAt)
                html += '<div id="comment-'+str(comment.id)+'" class="comment clearfix">'
                if comment.user.image:
                    html += '<img src="'+str(comment.user.image.url)+'" class="comment-img  float-left" width="50" height="50">'
                else:
                    html += '<img src="'+str(settings.SITE_URL)+str(settings.STATIC_URL)+'assets/img/avatar.jpeg" class="comment-img  float-left" width="50" height="50">'
                html += '<h5><a>'+str(comment.user.first_name)+' '+str(comment.user.last_name)+'</a></h5>'
                html += '<time>'+str(createdAt)+'</time>'
                html += '<p>'+str(comment.comment)+'</p>'
                html += '</div>'
            has_next = ''
            
            if comments.has_next():
                has_next = comments.next_page_number()

            return HttpResponse(json.dumps({"status": "success","data":html,'has_next':has_next,'total_comments':total_comments}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({"status": "error"}),content_type="application/json")
    except Exception as e:
        db_logger.exception(e)
        return HttpResponse(json.dumps({"status": "error"}),content_type="application/json")

#post comment
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def blog_comments(request, pk):
    try:
        blog            = get_object_or_404(Blog, pk=pk)
        total_comments  = BlogComment.objects.filter(blog=blog).count()
        records         = BlogComment.objects.filter(blog=blog).order_by('-id')
        paginator       = Paginator(records, settings.PER_PAGE_RECORD)
        page            = request.GET.get('page')
        comments        = paginator.get_page(page)

        html = ''
        for comment in comments:
            createdAt = time_ago(comment.createdAt)
            html += '<div id="comment-'+str(comment.id)+'" class="comment clearfix">'
            if comment.user.image:
                html += '<img src="'+str(comment.user.image.url)+'" class="comment-img  float-left" width="50" height="50">'
            else:
                html += '<img src="'+str(settings.SITE_URL)+str(settings.STATIC_URL)+'assets/img/avatar.jpeg" class="comment-img  float-left" width="50" height="50">'
            html += '<h5><a>'+str(comment.user.first_name)+' '+str(comment.user.last_name)+'</a></h5>'
            html += '<time>'+str(createdAt)+'</time>'
            html += '<p>'+str(comment.comment)+'</p>'
            html += '</div>'
        has_next = ''
        if comments.has_next():
            has_next = comments.next_page_number()
        return HttpResponse(json.dumps({"status": "success","data":html,'has_next':has_next,'total_comments':total_comments}),content_type="application/json")
    except Exception as e:
        db_logger.exception(e)
        return HttpResponse(json.dumps({"status": "error"}),content_type="application/json")