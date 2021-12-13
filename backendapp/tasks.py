from celery import Celery
from celery import shared_task
from celery import task
from accountapp.models import *
from jobapp.models import *
from fcm_django.models import FCMDevice
from datetime import datetime, timedelta
import time
import json
from urllib.request import urlopen
import http.client
from html import unescape
from django.core.mail.message import EmailMultiAlternatives
from django.template.exceptions import TemplateDoesNotExist
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.template.loader import get_template, render_to_string
from time import sleep
from twilio.rest import Client
import logging
import stripe
from django.core.mail import send_mail
db_logger = logging.getLogger('backendapp')

app = Celery()

#Send Temporary Password Email Task
@shared_task
def send_temporary_password_email_task(userid, password):
     try:
          user = User.objects.filter(pk=userid).first()

          context = {
          'first_name': user.first_name,
          'last_name': user.last_name,
          'email': user.email,
          'password': password,
          'SITE_URL' : settings.SITE_URL,
          'SITE_NAME' : settings.SITE_NAME,
          }

          template_subject ='email/password_reset/subject.txt'
          template_body    ='email/password_reset/body.txt'
          template_html    ='email/password_reset/body.html'
          subject          = loader.render_to_string(template_subject, context)
          text_body        = render_to_string(template_body, context=context)
          html_body        = render_to_string(template_html, context=context)
          # Email subject *must not* contain newlines
          subject          = ''.join(subject.splitlines())
          send_mail        = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[context['email']])
          send_mail.attach_alternative(html_body,'text/html')
          send_mail.send()
          return True
     except Exception as e:
          db_logger.exception(e)
          return str(e)

#send reset password email task
@shared_task
def send_reset_password_email_task(userid):
     try:
          user        = User.objects.filter(pk=userid).first()
          uid         = urlsafe_base64_encode(force_bytes(user.pk))
          token       = default_token_generator.make_token(user)
          reset_url   = str(settings.SITE_URL)+'/reset/'+str(uid)+'/'+str(token)+'/'
          
          context = {
          'email': user.email,
          'reset_url': reset_url,
          'user': user,
          'uid': urlsafe_base64_encode(force_bytes(user.pk)),
          'token': default_token_generator.make_token(user),
          'SITE_URL' : settings.SITE_URL,
          'SITE_NAME' : settings.SITE_NAME,
          }

          template_subject        ='email/password_reset_web/subject.txt'
          template_body           ='email/password_reset_web/body.txt'
          template_html           ='email/password_reset_web/body.html'
          subject                 = loader.render_to_string(template_subject, context)
          text_body               = render_to_string(template_body, context=context)
          html_body               = render_to_string(template_html, context=context)
          # Email subject *must not* contain newlines
          subject                 = ''.join(subject.splitlines())
          send_mail               = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[context['email']])
          send_mail.attach_alternative(html_body,'text/html')
          send_mail.send()
          return True

     except Exception as e:
          db_logger.exception(e)
          return str(e)

#send joboffer action email to employer
@shared_task
def send_joboffer_action_email_employer_task(pk):
     try:
          joboffer = JobOffer.objects.filter(pk=pk).first()
          #insert log
          notification             = Notification()
          notification.message     = 'Action on job offer'
          notification.user        = joboffer.job.user
          notification.save()
          context = {
          'SITE_URL' : settings.SITE_URL,
          'SITE_NAME' : settings.SITE_NAME,
          'joboffer' : joboffer,
          }
          template_subject        ='email/action/subject.txt'
          template_body           ='email/action/body.txt'
          template_html           ='email/action/body.html'
          subject                 = loader.render_to_string(template_subject, context)
          text_body               = render_to_string(template_body, context=context)
          html_body               = render_to_string(template_html, context=context)
          # Email subject *must not* contain newlines
          subject                 = ''.join(subject.splitlines())
          send_mail               = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[joboffer.job.user.email])
          send_mail.attach_alternative(html_body,'text/html')
          send_mail.send()
          return True

     except Exception as e:
          db_logger.exception(e)
          return str(e)

#send push notification task
@app.task
def send_notification_to_jobseeker_task(pk):
     try:
          joboffer = JobOffer.objects.filter(pk=pk).first()

          offermessage = "You have a New Job Offer"
          #insert log
          unreadoffer              = JobOffer.objects.filter(user=joboffer.user, IsRead = False).count()
          notification             = Notification()
          notification.message     = offermessage
          notification.user        = joboffer.user
          notification.save()
          
          #send email
          try:
               context = {
               'SITE_URL' : settings.SITE_URL,
               'SITE_NAME' : settings.SITE_NAME,
               'joboffer' : joboffer,
               }
               template_subject        ='email/hire/subject.txt'
               template_body           ='email/hire/body.txt'
               template_html           ='email/hire/body.html'
               subject                 = loader.render_to_string(template_subject, context)
               text_body               = render_to_string(template_body, context=context)
               html_body               = render_to_string(template_html, context=context)
               # Email subject *must not* contain newlines
               subject                 = ''.join(subject.splitlines())
               send_mail               = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[joboffer.user.email])
               send_mail.attach_alternative(html_body,'text/html')
               send_mail.send()
          except Exception as e:
               db_logger.exception(e)
               pass
          #send push to devices
          try:
               devices = FCMDevice.objects.filter(user=joboffer.user, active=True)
               if devices:
                    title = 'Job Offer'
                    body  = offermessage
                    db_logger.info("Send pushnotification send on token :"+str(joboffer.token))
                    sm = devices.send_message(title=title, body=body, badge=unreadoffer, sound=True, data={'offerid':str(joboffer.token),'token':str(joboffer.token)})
                    db_logger.info(sm)
          except Exception as e:
               db_logger.exception(e)
               pass
          #send text
          try:
               if joboffer.user.mobile:
                    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                    #client.messages.create(to="+91"+str(joboffer.user.mobile), from_= settings.TWILIO_PHONE_NUMBER, body=offermessage)
                    client.messages.create(to="+1"+str(joboffer.user.mobile), from_= settings.TWILIO_PHONE_NUMBER, body=offermessage)
          except Exception as e:
               db_logger.exception(e)
               pass
          
          return True
     except Exception as e:
          db_logger.exception(e)
          return str(e)

#contact us email task
@shared_task
def contact_us_email_task(pk):
     try:
          contact = ContactUs.objects.filter(pk=pk).first()
          context = {
          'SITE_URL' : settings.SITE_URL,
          'SITE_NAME' : settings.SITE_NAME,
          'contact' : contact,
          }
          template_subject        ='email/contact/user/subject.txt'
          template_body           ='email/contact/user/body.txt'
          template_html           ='email/contact/user/body.html'
          subject                 = loader.render_to_string(template_subject, context)
          text_body               = render_to_string(template_body, context=context)
          html_body               = render_to_string(template_html, context=context)
          # Email subject *must not* contain newlines
          subject                 = ''.join(subject.splitlines())
          send_mail               = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[contact.email])
          send_mail.attach_alternative(html_body,'text/html')
          send_mail.send()
          return True

     except Exception as e:
          db_logger.exception(e)
          return str(e)

#subscription email task
@shared_task
def subscription_email_task(pk):
     try:
          subscription = Subscription.objects.filter(pk=pk).first()
          context = {
          'SITE_URL' : settings.SITE_URL,
          'SITE_NAME' : settings.SITE_NAME,
          'subscription' : subscription,
          }
          template_subject        ='email/subscription/user/subject.txt'
          template_body           ='email/subscription/user/body.txt'
          template_html           ='email/subscription/user/body.html'
          subject                 = loader.render_to_string(template_subject, context)
          text_body               = render_to_string(template_body, context=context)
          html_body               = render_to_string(template_html, context=context)
          # Email subject *must not* contain newlines
          subject                 = ''.join(subject.splitlines())
          send_mail               = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[subscription.user.email])
          send_mail.attach_alternative(html_body,'text/html')
          send_mail.send()
          return True

     except Exception as e:
          db_logger.exception(e)
          return str(e)

#payroll service email
@shared_task
def payroll_service_email_task(user_id):
     try:
          user = User.objects.filter(pk=user_id).first()
          context = {
          'SITE_URL' : settings.SITE_URL,
          'SITE_NAME' : settings.SITE_NAME,
          'user' : user,
          }
          template_subject        ='email/payroll_service/user/subject.txt'
          template_body           ='email/payroll_service/user/body.txt'
          template_html           ='email/payroll_service/user/body.html'
          subject                 = loader.render_to_string(template_subject, context)
          text_body               = render_to_string(template_body, context=context)
          html_body               = render_to_string(template_html, context=context)
          # Email subject *must not* contain newlines
          subject                 = ''.join(subject.splitlines())
          send_mail               = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[user.email])
          send_mail.attach_alternative(html_body,'text/html')
          send_mail.send()
          #send to admin
          template_subject        ='email/payroll_service/admin/subject.txt'
          template_body           ='email/payroll_service/admin/body.txt'
          template_html           ='email/payroll_service/admin/body.html'
          subject                 = loader.render_to_string(template_subject, context)
          text_body               = render_to_string(template_body, context=context)
          html_body               = render_to_string(template_html, context=context)
          # Email subject *must not* contain newlines
          subject                 = ''.join(subject.splitlines())
          send_mail               = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,['adam@rezzame.com','notionmind.dev@gmail.com'])
          send_mail.attach_alternative(html_body,'text/html')
          send_mail.send()
          return True

     except Exception as e:
          db_logger.exception(e)
          return str(e)

#subscription reminder
@shared_task
def subscription_reminder(remider_days=1):
     try:
          db_logger.info('Subscription reminder cronjob start at: '+str(datetime.now()))
          remider_days = int(remider_days)
          subscriptions = Subscription.objects.filter(active=True, expired=False, cancel_at_period_end=True).order_by('enddate')
          if subscriptions:
               for subscription in subscriptions:
                    todayDate   = datetime.now().strftime('%Y-%m-%d')
                    expiredDate = subscription.enddate - timedelta(days=remider_days)
                    if str(expiredDate) == str(todayDate):
                         context = {
                         'SITE_URL' : settings.SITE_URL,
                         'SITE_NAME' : settings.SITE_NAME,
                         'subscription' : subscription,
                         }
                         template_subject ='email/subscription/reminder/subject.txt'
                         template_body    ='email/subscription/reminder/body.txt'
                         template_html    ='email/subscription/reminder/body.html'
                         subject          = loader.render_to_string(template_subject, context)
                         text_body        = render_to_string(template_body, context=context)
                         html_body        = render_to_string(template_html, context=context)
                         # Email subject *must not* contain newlines
                         subject          = ''.join(subject.splitlines())
                         send_mail        = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[subscription.user.email])
                         send_mail.attach_alternative(html_body,'text/html')
                         send_mail.send()
                         db_logger.info('Send reminder to '+str(subscription.user.company))
          db_logger.info('Subscription reminder cronjob stop at: '+str(datetime.now()))
          return True
     except Exception as e:
          db_logger.exception(e)
          return str(e)

#subscription billing reminder
@shared_task
def subscription_billing_reminder(remider_days=1):
     try:
          db_logger.info('Subscription billing reminder cronjob start at: '+str(datetime.now()))
          remider_days = int(remider_days)
          subscriptions = Subscription.objects.filter(active=True, expired=False, cancel_at_period_end=False).order_by('enddate')
          if subscriptions:
               for subscription in subscriptions:
                    todayDate   = datetime.now().strftime('%Y-%m-%d')
                    expiredDate = subscription.enddate - timedelta(days=remider_days)
                    if str(expiredDate) == str(todayDate):
                         context = {
                         'SITE_URL' : settings.SITE_URL,
                         'SITE_NAME' : settings.SITE_NAME,
                         'subscription' : subscription,
                         }
                         template_subject ='email/subscription/billing_reminder/subject.txt'
                         template_body    ='email/subscription/billing_reminder/body.txt'
                         template_html    ='email/subscription/billing_reminder/body.html'
                         subject          = loader.render_to_string(template_subject, context)
                         text_body        = render_to_string(template_body, context=context)
                         html_body        = render_to_string(template_html, context=context)
                         # Email subject *must not* contain newlines
                         subject          = ''.join(subject.splitlines())
                         send_mail        = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[subscription.user.email])
                         send_mail.attach_alternative(html_body,'text/html')
                         send_mail.send()
                         db_logger.info('Send billing reminder to '+str(subscription.user.company))
          db_logger.info('Subscription billing reminder cronjob stop at: '+str(datetime.now()))
          return True
     except Exception as e:
          db_logger.exception(e)
          return str(e)

#subscription expired
@shared_task
def subscription_membership_expired():
     try:
          db_logger.info('Subscription expired cronjob start at: '+str(datetime.now()))
          subscriptions = Subscription.objects.filter(active=True, expired=False, cancel_at_period_end=True).order_by('enddate')
          if subscriptions:
               for subscription in subscriptions:
                    todayDate   = datetime.now().date()
                    expiredDate = subscription.enddate
                    if expiredDate < todayDate:
                         context = {
                         'SITE_URL' : settings.SITE_URL,
                         'SITE_NAME' : settings.SITE_NAME,
                         'subscription' : subscription,
                         }
                         template_subject ='email/subscription/expired/subject.txt'
                         template_body    ='email/subscription/expired/body.txt'
                         template_html    ='email/subscription/expired/body.html'
                         subject          = loader.render_to_string(template_subject, context)
                         text_body        = render_to_string(template_body, context=context)
                         html_body        = render_to_string(template_html, context=context)
                         # Email subject *must not* contain newlines
                         subject          = ''.join(subject.splitlines())
                         send_mail        = EmailMultiAlternatives(subject,text_body,settings.DEFAULT_FROM_EMAIL,[subscription.user.email])
                         send_mail.attach_alternative(html_body,'text/html')
                         send_mail.send()

                         subscription.expired = True
                         subscription.save()

                         db_logger.info('Subscription expired of '+str(subscription.user.company))
                    db_logger.info('Subscription expired cronjob stop at: '+str(datetime.now()))
          return True
     except Exception as e:
          db_logger.exception(e)
          return str(e)

#subscription expired
@shared_task
def subscription_billing_expired():
     try:
          stripe.api_key = settings.STRIPE_SECRET_KEY # new
          db_logger.info('Subscription billing expired cronjob start at: '+str(datetime.now()))
          subscriptions = Subscription.objects.filter(active=True, expired=False, cancel_at_period_end=False).order_by('enddate')
          if subscriptions:
               for subscription in subscriptions:
                    todayDate   = datetime.now().date()
                    expiredDate = subscription.enddate
                    if expiredDate < todayDate:
                         db_logger.info('Subscription billing expired of '+str(subscription.user.company))
                    db_logger.info('Subscription billing expired cronjob stop at: '+str(datetime.now()))
          return True
     except Exception as e:
          db_logger.exception(e)
          return str(e)