from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, logout, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator
from .forms import *
from accountapp.models import *
from blogapp.models import *
from accountapp.decorator import *
from jobapp.models import *
from backendapp.sendmail import *
from backendapp.latlong import *
from django.http.response import  HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, SetPasswordForm
from django.views.decorators.cache  import cache_control
import logging
import requests
from datetime import datetime, timedelta
from dateutil.relativedelta import *
from django.db.models import Count, Q
from django.conf import settings
from django.core.paginator import Paginator
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F
import os

db_logger = logging.getLogger('accountapp')

stripe.api_key = settings.STRIPE_SECRET_KEY # new

# home
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    try:
        context  = {}
        return render(request, 'home.html', context)
    except Exception as e:
        db_logger.exception(e)
        return e

# how_it_works
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def how_it_works(request):
    try:
        context  = {}
        return render(request, 'how-it-works.html', context)
    except Exception as e:
        db_logger.exception(e)
        return e

# access denied
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def access_denied(request):
    try:
        context  = {}
        return render(request, 'access_denied.html', context)
    except Exception as e:
        db_logger.exception(e)
        return e

# sign in
def sign_in(request):
    try:
        #already login user
        if request.user.is_authenticated:
                return redirect(str(settings.SITE_URL)+'/dashboard')
        #check post login user
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                info = User.objects.filter(email = username, groups__name='Employer').first()
                user = authenticate(email=info.email, password=password)
                if user is not None:
                    login(request, user)
                    db_logger.info(str(username)+" is successfully sign in")
                    return redirect(str(settings.SITE_URL)+'/dashboard')
                else:
                    db_logger.warning(str(username)+" is not found")
                    messages.error(request, str(username)+" is not found")
                    return redirect(str(settings.SITE_URL)+'/sign-in')
        else:
            form = LoginForm()
        
        context = {"form": form,}
        return render(request, 'sign-in.html', context)

    except Exception as e:
            db_logger.exception(e)
            return e

# logout page
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sign_out(request):
    try:
        username = request.user.email
        logout(request)
        db_logger.info(str(username)+" is successfully sign out")
        return HttpResponseRedirect(str(settings.SITE_URL)+'/sign-in')
    except Exception as e:
            db_logger.exception(e)
            return e

#sign up
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sign_up(request, template_name='sign-up.html'):
    try:
        #already login user
        if request.user.is_authenticated:
            return redirect(str(settings.SITE_URL)+'/dashboard')

        if request.method == 'POST':
            form = RegisterForm(request.POST, request.FILES)
            if form.is_valid():
                ''' Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                # result = r.json()
                ''' End reCAPTCHA validation '''
                # By Pass Captacha 
                result={
                    'success':True
                }

                if result['success']:
                    user = form.save()
                    user.set_password(request.POST['password1'])
                    #save user group
                    group = Group.objects.get(name='Employer')
                    user.groups.add(group)
                    #save user group
                    user.ipaddress      = request.META['REMOTE_ADDR']
                    user.browserinfo    = request.META['HTTP_USER_AGENT']
                    user.save()
                    user = authenticate(email=user.email, password=request.POST['password1'])
                    login(request, user)
                    return redirect(str(settings.SITE_URL)+'/dashboard')
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        else:
            form = RegisterForm(request.POST or None)
        return render(request, template_name, {'form':form, 'recaptcha_site_key' : settings.GOOGLE_RECAPTCHA_SITE_KEY})
    except Exception as e:
            db_logger.exception(e)
            return e

# - Reset Password Request
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email    = request.POST['email']
            email    = email.lower()
            user     = User.objects.filter(email=email).first()
            #send email
            send_reset_password_email(request,user)
            return redirect(str(settings.SITE_URL)+'/password_reset/done/')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordResetRequestForm(request.POST or None)

    return render(request, 'password_reset_form.html', {
        'form': form
    })

# - Reset Password done
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def password_reset_done(request):
    return render(request, 'password_reset_done.html')

# - Reset Password done
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def password_reset_confirm(request, uid, token):

    try:
        # urlsafe_base64_decode() decodes to bytestring on Python 3
        uid = force_text(urlsafe_base64_decode(uid))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        validlink = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return redirect(str(settings.SITE_URL)+'/reset/done/')
        else:
            form = SetPasswordForm(user)
    else:
        validlink = False
        form = None
    
    context = {
        'form': form,
        'validlink': validlink,
    }
    return render(request, 'password_reset_confirm.html',context)

# - Reset Password done
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def password_reset_complete(request):
    return render(request, 'password_reset_complete.html')

# Dashboard
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard(request):
    try:
        context                 =   {}
        subscription            =   Subscription.objects.filter(user=request.user, status='Current', expired=False, active=True).first()
        isSubscription          = False
        if subscription:
            isSubscription      = True
        context['isSubscription']   =   isSubscription
        return render(request, 'dashboard.html', context)
    except Exception as e:
        db_logger.exception(e)
        return e

#profile
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def profile(request):
    try:
        #check post user
        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile has been updated successfully!')
                return redirect(str(settings.SITE_URL)+'/profile')
        else:
            form = ProfileForm(request.POST or None, instance=request.user)
        
        context = {"form": form,}
        return render(request, 'profile.html', context)

    except Exception as e:
            db_logger.exception(e)
            return e

#change password
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
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
                return redirect(str(settings.SITE_URL)+'/change-password')
        else:
            form = PasswordChangeForm(request.user)
        
        context = {"form": form,}
        return render(request, 'change-password.html', context)

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

#find job seekers
# @login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
# @check_role_permission() # - check role permission
# @check_subscription_permission() # - check subscription
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def find_job_seekers(request, template_name='jobseeker/listing.html'):
    try:
        #get post
        if request.method == 'POST':
            if 'clearbtn' in request.POST:
                #clear form
                if 'job-seeker-search-post' in request.session:
                    del request.session['job-seeker-search-post']
                if 'job_seeker_category' in request.session:
                    del request.session['job_seeker_category']
                return redirect(str(settings.SITE_URL)+'/find-job-seekers')
            else:
                request.session['job-seeker-search-post']   = request.POST
                Post_Data                                   = request.POST
                job_seeker_category                         = []
                if 'category' in request.POST:
                    request.session['job_seeker_category']      = request.POST.getlist('category')
                    job_seeker_category                         = request.POST.getlist('category')    

        else:
            if 'job-seeker-search-post' in request.session:
                Post_Data = request.session['job-seeker-search-post']
            else:
                Post_Data = []

            if 'job_seeker_category' in request.session:
                job_seeker_category = request.session['job_seeker_category']
            else:
                job_seeker_category = []

        #check session
        if Post_Data:
            form = JobSeekerFilter(Post_Data)
        else:
            form = JobSeekerFilter()

        complexQuery   = Q(is_staff=False, is_superuser=False, is_active=True, groups__name='Jobseeker', IsProComplete=True)

        if Post_Data:
            search      = Post_Data['search'] if Post_Data['search'] else ''
            radius      = Post_Data['radius'] if Post_Data['radius'] else ''
            
            if job_seeker_category:
                users = []
                categories = UserCategory.objects.filter(category__id__in=job_seeker_category)
                if categories:
                    for uc in categories:
                        if uc.user.id not in users:
                            users.append(uc.user.id)
                if users:
                    complexQuery.add(Q(id__in=users), complexQuery.AND)

            if radius and search:
                current_location = find_zipcode(search)
                if current_location:
                    dlat = Radians(F('latitude') - current_location['latitude'])
                    dlong = Radians(F('longitude') - current_location['longitude'])
                    a = (Power(Sin(dlat/2), 2) + Cos(Radians(current_location['latitude'])) 
                        * Cos(Radians(F('latitude'))) * Power(Sin(dlong/2), 2)
                    )
                    c = 2 * ATan2(Sqrt(a), Sqrt(1-a))
                    d = 6371 * c
                    objs  = User.objects.annotate(distance=d).order_by('distance').filter(distance__lt=radius).filter(complexQuery)
                else:
                    objs  = User.objects.filter(complexQuery).order_by('-available')
            elif search:
                complexQuery.add(Q(state__name__icontains=search) | Q(state__code__icontains=search) | Q(city__name__icontains=search) | Q(zipcode__icontains=search), complexQuery.AND)
                objs  = User.objects.filter(complexQuery).order_by('-available')
            else:
                objs  = User.objects.filter(complexQuery).order_by('-available')
        else:
                objs  = User.objects.filter(complexQuery).order_by('-available')
        
        paginator   = Paginator(objs, settings.PER_PAGE_RECORD)
        page        = request.GET.get('page')
        records     = paginator.get_page(page)
        # records=User.objects.all()
        data = {}
        data['object_list']     = records
        data['form']            = form
        return render(request, template_name, data)
    except Exception as e:
            print("*************************************************")
            print(e)
            print("*************************************************")

            db_logger.exception(e)
            return e

# #profile
# @login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
# @check_role_permission() # - check role permission
# @check_subscription_permission() # - check subscription
# @cache_control(no_cache=True, must_revalidate=True, no_store=True)
def job_seeker_profile(request, token):
    try:
        context             = {}
        record              = get_object_or_404(User, is_staff=False, is_superuser=False, is_active=True, groups__name='Jobseeker', token=token)
        if request.method == 'POST':
            job_token   = request.POST.get('job')
            if job_token:
                instruction = ''
                if 'instruction' in request.POST:
                    instruction = request.POST.get('instruction')
                job  = Job.objects.filter(user=request.user, token=job_token, publish=True).first()
                
                subscription    = Subscription.objects.filter(user=job.user,status='Current').first()
                if subscription is None:
                    subscription     = Subscription.objects.filter(user=job.user).last()
                
                #save offer
                offer               = JobOffer()
                offer.user          = record
                offer.job           = job
                if subscription:
                    offer.subscription = subscription
                if instruction:
                    offer.instruction = instruction
                offer.ipaddress     = request.META['REMOTE_ADDR']
                offer.browserinfo   = request.META['HTTP_USER_AGENT']
                offer.createdBy     = request.user
                offer.save()
                #send notification, text message and email to jobseeker
                send_notification_to_jobseeker(offer)
                
                messages.success(request,"Request has been sent successfully.")
                return redirect(str(settings.SITE_URL)+'/job-seeker/'+str(token))
            else:
                messages.error(request,"Invalid request.")
                return redirect(str(settings.SITE_URL)+'/job-seeker/'+str(token))

        jobs = Job.objects.filter(user=request.user, publish=True).order_by('-id')
        if jobs:
            for job in jobs:
                job.offer = JobOffer.objects.filter(job=job,user=record).first()
        video_url = ''
        if record.video:
            basename = os.path.basename(record.video.url)
            video_url = 'https://gotoworkamerica.com:9001/'+str(basename)

        context['object']       = record
        context['video_url']    = video_url
        context['jobs']         = jobs
        #view by
        userprofileview             = UserProfileView()
        userprofileview.user        = record
        userprofileview.viewby      = request.user
        userprofileview.ipaddress   = request.META['REMOTE_ADDR']
        userprofileview.browserinfo = request.META['HTTP_USER_AGENT']
        userprofileview.save()
        return render(request, 'jobseeker/profile.html', context)
    except Exception as e:
        db_logger.exception(e)
        return e

#sign up
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def contact_us(request, template_name='contact_us.html'):
    try:
        if request.method == 'POST':
            form = ContactUsForm(request.POST)
            if form.is_valid():
                ''' Begin reCAPTCHA validation '''
                recaptcha_response = request.POST.get('g-recaptcha-response')
                data = {
                    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                    'response': recaptcha_response
                }
                r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
                result = r.json()
                ''' End reCAPTCHA validation '''
                if result['success']:
                    contact = form.save()
                    if request.user.is_authenticated:
                        contact.user  = request.user
                    contact.ipaddress      = request.META['REMOTE_ADDR']
                    contact.browserinfo    = request.META['HTTP_USER_AGENT']
                    contact.save()
                    #send mail
                    contact_us_email(contact)
                    messages.success(request,"Thank you for contact us.")
                    return redirect(str(settings.SITE_URL)+'/contact-us')
                else:
                    messages.error(request, 'Invalid reCAPTCHA. Please try again.')
        else:
            form = ContactUsForm(request.POST or None)
        return render(request, template_name, {'form':form, 'recaptcha_site_key' : settings.GOOGLE_RECAPTCHA_SITE_KEY})
    except Exception as e:
            db_logger.exception(e)
            return e

#subscription
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription(request, template_name='subscription/list.html'):
    try:
        #response = stripe.Subscription.retrieve(record.stripe_subscription_id)
        context                 =   {}
        current                 =   Subscription.objects.filter(user=request.user,status='Current').first()
        records                 =   Subscription.objects.filter(user=request.user,status='Old').order_by('-id')
        context['object_list']  =   records
        context['current']      =   current
        return render(request, template_name, context)
    except Exception as e:
            db_logger.exception(e)
            return e

#subscription thank you
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_plan(request, template_name='subscription/plan.html'):
    try:
        context                 =   {}
        records                 =   Plan.objects.filter(publish=True).order_by('-id')
        context['object_list']  =   records
        return render(request, template_name, context)
    except Exception as e:
            db_logger.exception(e)
            return e

#subscription new
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_checkout(request, plan, template_name='subscription/checkout.html'):
    try:
        plan_info  =   Plan.objects.filter(publish=True, token=plan).first()
        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': plan_info.productid,
                'quantity': 1,
            }],
            metadata={
                "product_id": plan_info.token
            },
            mode='subscription',
            allow_promotion_codes=True,
            success_url=str(settings.SITE_URL)+'/subscription/success/'+str(plan)+'?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=str(settings.SITE_URL)+'/subscription/back/'+str(plan),
        )
        return render(request, template_name, {'plan' : plan_info, 'stripe_publishable_key' : settings.STRIPE_PUBLISHABLE_KEY, 'session_id': session.id})
    except Exception as e:
            db_logger.exception(e)
            return e

#subscription thank you
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_success(request, plan, template_name='subscription/success.html'):
    try:
        plan_info  =   Plan.objects.filter(publish=True, token=plan).first()
        if request.method == 'GET' and 'session_id' in request.GET:
            session  = stripe.checkout.Session.retrieve(request.GET['session_id'],)
            if session:
                context            =    {}
                context['object']  =    plan_info
                return render(request, template_name, context)
            else:
                db_logger.error(session)
                messages.error(request, 'Invalid Session ID, Please try again.')
                return redirect(str(settings.SITE_URL)+'/subscription/'+str(plan))
        else:
            messages.error(request, 'Invalid Request, Please try again.')
            return redirect(str(settings.SITE_URL)+'/subscription/plan')
    except Exception as e:
        db_logger.exception(e)
        return e

#subscription expired
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_expired(request, template_name='subscription/expired.html'):
    try:
        context            =    {}
        record             =    Subscription.objects.filter(user=request.user).last()
        context['object']  =    record
        return render(request, template_name, context)
    except Exception as e:
        db_logger.exception(e)
        return e

#subscription inactive
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_inactive(request, template_name='subscription/inactive.html'):
    try:
        context            =    {}
        record             =    Subscription.objects.filter(user=request.user).last()
        context['object']  =    record
        return render(request, template_name, context)
    except Exception as e:
        db_logger.exception(e)
        return e

#subscription cancel
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_cancel(request, template_name='subscription/cancel.html'):
    try:
        context            =    {}
        record             =    Subscription.objects.filter(user=request.user, status='Current', cancel_at_period_end = False, payment_type='Online').first()
        if request.method=='POST':
                response = stripe.Subscription.modify(record.stripe_subscription_id,cancel_at_period_end=True)
                db_logger.info('Subscription cancel by '+str(request.user.email))
                if response:
                    db_logger.info(response)
                    timestamp                   = response['current_period_end']
                    enddate                     = datetime.fromtimestamp(timestamp)
                    record.cancel_at_period_end = True
                    record.canceldate           = datetime.now()
                    record.enddate              = enddate
                    record.save()
                    messages.success(request, 'Your subscription has been successfully canceled')
                    return redirect(str(settings.SITE_URL)+'/subscription')
                else:
                    db_logger.error(response)
                    messages.error(request, 'Invalid request')
                    return redirect(str(settings.SITE_URL)+'/subscription/cancel')
        context['object']  =    record
        return render(request, template_name, context)
    except Exception as e:
        db_logger.exception(e)
        return e

#subscription back
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def subscription_back(request, plan):
    try:
        return redirect(str(settings.SITE_URL)+'/subscription/'+str(plan)+'/checkout')
    except Exception as e:
        db_logger.exception(e)
        return e

#allow location
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def allow_location(request, latitude, longitude):
    try:
        request.session['current_location']  = {'latitude' :  float(latitude), 'longitude' :  float(longitude)}
        return HttpResponse('Success')
    except Exception as e:
        db_logger.exception(e)
        return e

#denied location
@login_required(login_url=str(settings.SITE_URL)+'/sign-in') # - if not logged in redirect to /
@check_role_permission() # - check role permission
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def denied_location(request):
    try:
        if 'current_location' in request.session:
            del request.session['current_location']
        return HttpResponse('Success')
    except Exception as e:
        db_logger.exception(e)
        return e

#language chnage
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def language(request, lang):
    try:
        return HttpResponse('Success')
    except Exception as e:
        db_logger.exception(e)
        return e

#stripe webhook
@csrf_exempt
def stripe_webhook(request):
    try:
        db_logger.info('Subscription webhook data :'+str(request.body))
        payload     = request.body
        sig_header  = request.META['HTTP_STRIPE_SIGNATURE']
        event       = None
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except ValueError as e:
            db_logger.exception(e)
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            db_logger.exception(e)
            return HttpResponse(status=400)
        # Handle the checkout.session.completed event
        if event['type'] == 'checkout.session.completed':
            session         = event['data']['object']
            db_logger.info('Session:'+str(session))
            customer_email  = session["customer_details"]["email"]
            user            = User.objects.get(email = customer_email)
            product_id      = session["metadata"]["product_id"]
            plan_info       = Plan.objects.get(token=product_id)
            db_logger.info('Subscription purchase by : '+str(customer_email))
            if session:
                db_logger.info('Subscription session : '+str(session))
                startdate  = datetime.now()
                if plan_info.period == 'yearly':
                    enddate = startdate + relativedelta(months=+12)
                elif plan_info.period == 'half-yearly':
                    enddate = startdate + relativedelta(months=+6)
                elif plan_info.period == 'quarterly':
                    enddate = startdate + relativedelta(months=+3)
                else:
                    enddate = startdate + relativedelta(months=+1)
                #change old subscription status
                old_subscription = Subscription.objects.filter(user=user,status='Current').first()
                if old_subscription:
                    old_subscription.status = 'Old'
                    old_subscription.save()
                subscription                        = Subscription()
                subscription.user                   = user
                subscription.plan                   = plan_info
                subscription.stripeid               = session.customer
                subscription.membership             = True
                subscription.cancel_at_period_end   = False
                subscription.stripe_subscription_id = session.subscription
                subscription.period                 = plan_info.period
                subscription.startdate              = startdate
                subscription.enddate                = enddate
                subscription.status                 = 'Current'
                subscription.payment_amount         = plan_info.amount
                subscription.payment_type           = 'Online'
                subscription.payment_status         = 'Success'
                subscription.payment_response       = session
                subscription.ipaddress              = request.META['REMOTE_ADDR']
                subscription.browserinfo            = request.META['HTTP_USER_AGENT']
                subscription.createdBy              = user
                subscription.save()
                #send email
                subscription_email(subscription)
        
        return HttpResponse(status=200)

    except Exception as e:

        db_logger.exception(e)
        return e

# sign in
def newsletter_subscription(request):
    try:
        #already login user
        if request.user.is_authenticated:
                return redirect(str(settings.SITE_URL)+'/dashboard')
        #check post login user
        if request.method == 'POST':
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                username = request.POST['username']
                password = request.POST['password']
                info = User.objects.filter(email = username, groups__name='Employer').first()
                user = authenticate(email=info.email, password=password)
                if user is not None:
                    login(request, user)
                    db_logger.info(str(username)+" is successfully sign in")
                    return redirect(str(settings.SITE_URL)+'/dashboard')
                else:
                    db_logger.warning(str(username)+" is not found")
                    messages.error(request, str(username)+" is not found")
                    return redirect(str(settings.SITE_URL)+'/sign-in')
        else:
            form = LoginForm()
        
        context = {"form": form,}
        return render(request, 'sign-in.html', context)

    except Exception as e:
            db_logger.exception(e)
            return e
