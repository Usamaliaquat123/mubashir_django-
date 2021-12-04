from django.core.mail.message import EmailMultiAlternatives
from django.template.exceptions import TemplateDoesNotExist
from django.template.loader import get_template, render_to_string
from backendapp.tasks import *
from accountapp.models import *
from jobapp.models import *
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template import loader
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
import requests
import logging
import os
from urllib.parse import urlparse
from email.mime.image import MIMEImage
import logging
import random
from twilio.rest import Client
BLOCK_SIZE  =   8

db_logger = logging.getLogger('apiapp')

def create_otp(arg=4):
    if arg == 6:
        return str(random.randint(100000, 999999))
    else:
        return str(random.randint(1000, 9999))

#send Temporary Password
def sendTemporaryPassword(request, user):
    try:
        #temp password
        password = create_otp(6)

        #insert log
        temp_pass_send                        =   TemporaryPassword()
        temp_pass_send.user                   =   user
        temp_pass_send.password               =   password
        temp_pass_send.device_id              =   request.data.get("device_id")
        temp_pass_send.source                 =   request.data.get("source")
        temp_pass_send.ipaddress              =   request.META['REMOTE_ADDR']
        temp_pass_send.browserinfo            =   request.META['HTTP_USER_AGENT']
        temp_pass_send.save()
        
        #send mail
        send_temporary_password_email_task.delay(user.id, password)

        return True
    except Exception as e:
        db_logger.exception(e)
        return True

#send reset password email
def send_reset_password_email(request, user):
    #send mail
    send_reset_password_email_task.delay(user.id)
    return True

#send notification, text message and email to jobseeker
def send_notification_to_jobseeker(joboffer):
    #send mail
    send_notification_to_jobseeker_task.delay(joboffer.id)
    return True

#send notification, text message and email to jobseeker
def send_joboffer_action_email_employer(joboffer):
    #send mail
    send_joboffer_action_email_employer_task.delay(joboffer.id)
    return True

#send notification, text message and email to jobseeker
def contact_us_email(contact):
    #send mail
    contact_us_email_task.delay(contact.id)
    return True

#send subscription email
def subscription_email(subscription):
    #send mail
    subscription_email_task.delay(subscription.id)
    return True

#send payroll service email
def send_payroll_service_email(user):
    #send mail
    payroll_service_email_task.delay(user.id)
    return True