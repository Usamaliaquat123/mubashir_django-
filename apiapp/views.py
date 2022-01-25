from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response, SimpleTemplateResponse
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from rest_framework.authtoken.models import Token

from backendapp.latlong import *
from backendapp.sendmail import *
from accountapp.models import *
from jobapp.models import *
from apiapp.permissions import hasKey
from apiapp.authentication import refresh_token
from apiapp.serializer import *

import time
import requests
import datetime
from datetime import timedelta
import time
import pytz
import logging
import uuid
import os
import json
from django.conf import settings
import logging
from urllib.request import urlopen
import http.client
from html import unescape
from django.utils.html import strip_tags
from fcm_django.models import FCMDevice
from django.core.files.base import ContentFile
from django.db.models import Q
db_logger = logging.getLogger('apiapp')

# user login
@api_view(["POST",])
@permission_classes((hasKey,))
def login(request):
    try:
        device_id    =   request.data.get("device_id")
        source       =   request.data.get("source")
        devicetoken  =   request.data.get("devicetoken")
        email       =    request.data.get("email")
        password    =    request.data.get("password")

        if not email or not password:
            return Response(data={"status":"Error","message":"Please enter email and password"}, status=HTTP_200_OK)
        try:
            user = get_user_model().objects.get(email=email,groups__name='Jobseeker')
            email= user.email
        except Exception as e:
            db_logger.exception(e)
            return Response(data={"status":"Error","message":"This email address not found"}, status=HTTP_200_OK)
        user = authenticate(email=email, password=password)
        #assert False
        if not user:
            return Response(data={"status":"Error","message":"Invalid password"}, status=HTTP_200_OK)
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            utc_now = datetime.datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)
            token.created = utc_now
            token.save()
        auth_login(request._request, user)
        
        #check pushnotification
        if devicetoken:
            source = source.lower()
            device = FCMDevice.objects.filter(user=user, device_id=device_id, type=source).first()
            #removed
            if device:
                device.delete()
            #add
            device = FCMDevice(name=source, user=user, device_id=device_id, registration_id=devicetoken, active=True, type=source)
            device.save()
        
        usersr = ProfileSerializer(get_user_model().objects.get(id=user.id))
        return Response(data={"status":"Success","message":"Logged In","token":token.key,"data":usersr.data}, status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":str(e)}, status=HTTP_200_OK)

# user logout
@api_view(["POST",])
def logout(request):
    if request.user:
        '''
        token = Token.objects.get(user=request.user)
        token.delete()
        '''
        device_id    =   request.data.get("device_id")
        source       =   request.data.get("source")
        if device_id:
            source = source.lower()
            device = FCMDevice.objects.filter(user=request.user, device_id=device_id, type=source).first()
            if device:
                device.delete()
        
        auth_logout(request._request)
    return Response(data={"status":"Success","message":"Logged Out"},status=HTTP_200_OK)

#state listing
@api_view(['GET',])
@permission_classes((hasKey,))
def states(request):
    try:
        data          = State.objects.filter(publish=True).order_by('name')
        serializer    = StateSerializer(data,many=True)
        return Response({"status":"Success","message":"Data loaded","data":serializer.data},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response({"status":"Error","message":"Unable to find data"},status=HTTP_200_OK)

#city listing
@api_view(['GET',])
@permission_classes((hasKey,))
def cities(request):
    try:
        state      = request.query_params.get('state_id')
        data       = City.objects.filter(state__id=state,publish=True).order_by('name')
        serializer = CitySerializer(data,many=True)
        return Response({"status":"Success","message":"Data loaded","data":serializer.data},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response({"status":"Error","message":"Unable to find data"},status=HTTP_200_OK)

#state listing
@api_view(['GET',])
@permission_classes((hasKey,))
def category(request):
    try:
        data          = Category.objects.filter(publish=True).order_by('name')
        serializer    = CategorySerializer(data,many=True)
        return Response({"status":"Success","message":"Data loaded","data":serializer.data},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response({"status":"Error","message":"Unable to find data"},status=HTTP_200_OK)

#city listing
@api_view(['GET',])
@permission_classes((hasKey,))
def subcategory(request):
    try:
        category   = request.query_params.get('category_id')
        data       = Subcategory.objects.filter(category__id=category,publish=True).order_by('name')
        serializer = SubCategorySerializer(data,many=True)
        return Response({"status":"Success","message":"Data loaded","data":serializer.data},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response({"status":"Error","message":"Unable to find data"},status=HTTP_200_OK)

#discover feeds listing
@api_view(["GET",])
@permission_classes((hasKey,))
def categories(request):
    try:
        categories_list   = []
        records       = Category.objects.filter(publish=True).order_by('name')
        for record in records:
            respose = {}
            respose['id']        = record.id
            respose['name']      = record.name
            subcategories_list   = []
            subs                 = Subcategory.objects.filter(category=record,publish=True).order_by('name')
            if subs:
                for sub in subs:
                    sub_respose = {}
                    sub_respose['id']        = sub.id
                    sub_respose['name']      = sub.name
                    subcategories_list.append(sub_respose)
            respose['subcategories']  = subcategories_list
            categories_list.append(respose)
        return Response(data={"status":"Success","message":"Loaded","data":categories_list},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":str(e)}, status=HTTP_200_OK)

#language listing
@api_view(['GET',])
@permission_classes((hasKey,))
def language(request):
    try:
        data          = Language.objects.filter(publish=True).order_by('name')
        serializer    = LanguageSerializer(data,many=True)
        return Response({"status":"Success","message":"Data loaded","data":serializer.data},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response({"status":"Error","message":"Unable to find data"},status=HTTP_200_OK)

#register listing
@api_view(['POST',])
@permission_classes((hasKey,))
def register(request):
    try:
        device_id    =   request.data.get("device_id")
        source       =   request.data.get("source")
        devicetoken  =   request.data.get("devicetoken")
        usersr       =   UserSerializer(data=request.data)
        if usersr.is_valid():
            usersr.save()
            password  = request.data.get("password")
            usersr.instance.source      = request.data.get("source")
            usersr.instance.ipaddress   = request.META['REMOTE_ADDR']
            usersr.instance.browserinfo = request.META['HTTP_USER_AGENT']
            usersr.instance.devicetoken = devicetoken
            usersr.instance.device_id   = device_id
            usersr.instance.IsProCompleteStatus   = 'Contact'
            usersr.save()
            
            #get user object
            user = usersr.instance
            user.set_password(password)
            user.save()

            #login
            token, created = Token.objects.get_or_create(user=user)
            if not created:
                utc_now = datetime.datetime.utcnow()
                utc_now = utc_now.replace(tzinfo=pytz.utc)
                token.created = utc_now
                token.save()
            auth_login(request._request, user)

            #check pushnotification
            if devicetoken:
                source = source.lower()
                device = FCMDevice.objects.filter(user=user, device_id=device_id, type=source).first()
                #removed
                if device:
                    device.delete()
                #add
                device = FCMDevice(name=source, user=user, device_id=device_id, registration_id=devicetoken, active=True, type=source)
                device.save()

            usersr = ProfileSerializer(get_user_model().objects.get(id=user.id))

            return Response(data={"status":"Success","message":"Registration has been successfully.","token":token.key,"data":usersr.data},status=HTTP_200_OK)
        
        errors = usersr.errors
        errormsg = ''
        
        for error in errors:
            errormsg += str(error)+' - '+str(errors[error][0])+'\n\n'
        
        if errormsg:
            errormsg = errormsg[:-3] 
        return Response(data={"status":"Error","message":errormsg},status=HTTP_200_OK)
    
    except Exception as e:
        
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Can't create user"},status=HTTP_400_BAD_REQUEST)

#update yourself
@api_view(["POST"])
def profile_yourself(request):
    try:
        refresh_token(request.user)
        usersr = profileYourselfSerializer(get_user_model().objects.get(id=request.user.id),data=request.data)
        if usersr.is_valid():
            usersr.save()
            usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
            return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
        
        errors = usersr.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

    except Exception as e:

        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

#update categories
@api_view(["POST"])
def profile_categories(request):
    try:
        refresh_token(request.user)
        categories = request.data.get('categories')
        subcategories = request.data.get('subcategories')
        if not categories:
            return Response(data={"status":"Error","message":"Please select atleast one category"}, status=HTTP_200_OK)
        
        if categories:
            #delete old categries
            deleted = UserCategory.objects.filter(user=request.user).delete()
            for category in categories:
                if category:
                    cat_user                = UserCategory()
                    cat_user.user           = request.user
                    cat_user.category_id    = category
                    cat_user.save()
                    if subcategories:
                        subs = Subcategory.objects.filter(category_id=category, id__in=subcategories)    
                        if subs:
                            for sub in subs:
                                if sub:
                                    cat_user.subcategory.add(sub)
        
        
        user = get_user_model().objects.get(id=request.user.id)
        user.IsProCompleteStatus   = 'Schedule'
        user.save()
        
        usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
        return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

# get profile
@api_view(["GET"])
def profile(request):
    try:
        refresh_token(request.user)
        usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
        return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        print("==============================")
        print(e)
        print("==============================")
        return Response(data={"status":"Error","message":"Invalid user","error":e}, status=HTTP_200_OK)

#update profile
@api_view(["POST"])
def update_profile(request):
    try:
        refresh_token(request.user)
        post_data = request.data
        
        if post_data['sun'] == False or  post_data['sun'] == 0:
            post_data['sun_start_hr'] = None
            post_data['sun_start_ap'] = None
            post_data['sun_end_hr']   = None
            post_data['sun_end_ap']   = None
        else:
            if post_data['sun_start_ap'] == 0:
                post_data['sun_start_ap'] = 'AM'
            elif post_data['sun_start_ap'] == 1:
                post_data['sun_start_ap'] = 'PM'
            else:
                post_data['sun_start_ap'] = None

            if post_data['sun_end_ap'] == 0:
                post_data['sun_end_ap'] = 'AM'
            elif post_data['sun_end_ap'] == 1:
                post_data['sun_end_ap'] = 'PM'
            else:
                post_data['sun_end_ap'] = None

        if post_data['mon'] == False:
            post_data['mon_start_hr'] = None
            post_data['mon_start_ap'] = None
            post_data['mon_end_hr']   = None
            post_data['mon_end_ap']   = None
        else:
            if post_data['mon_start_ap'] == 0:
                post_data['mon_start_ap'] = 'AM'
            elif post_data['mon_start_ap'] == 1:
                post_data['mon_start_ap'] = 'PM'
            else:
                post_data['mon_start_ap'] = None

            if post_data['mon_end_ap'] == 0:
                post_data['mon_end_ap'] = 'AM'
            elif post_data['mon_end_ap'] == 1:
                post_data['mon_end_ap'] = 'PM'
            else:
                post_data['mon_end_ap'] = None

        if post_data['tue'] == False:
            post_data['tue_start_hr'] = None
            post_data['tue_start_ap'] = None
            post_data['tue_end_hr']   = None
            post_data['tue_end_ap']   = None
        else:
            if post_data['tue_start_ap'] == 0:
                post_data['tue_start_ap'] = 'AM'
            elif post_data['tue_start_ap'] == 1:
                post_data['tue_start_ap'] = 'PM'
            else:
                post_data['tue_start_ap'] = None

            if post_data['tue_end_ap'] == 0:
                post_data['tue_end_ap'] = 'AM'
            elif post_data['tue_end_ap'] == 1:
                post_data['tue_end_ap'] = 'PM'
            else:
                post_data['tue_end_ap'] = None

        if post_data['wed'] == False:
            post_data['wed_start_hr'] = None
            post_data['wed_start_ap'] = None
            post_data['wed_end_hr']   = None
            post_data['wed_end_ap']   = None
        else:
            if post_data['wed_start_ap'] == 0:
                post_data['wed_start_ap'] = 'AM'
            elif post_data['wed_start_ap'] == 1:
                post_data['wed_start_ap'] = 'PM'
            else:
                post_data['wed_start_ap'] = None

            if post_data['wed_end_ap'] == 0:
                post_data['wed_end_ap'] = 'AM'
            elif post_data['wed_end_ap'] == 1:
                post_data['wed_end_ap'] = 'PM'
            else:
                post_data['wed_end_ap'] = None

        if post_data['thu'] == False:
            post_data['thu_start_hr'] = None
            post_data['thu_start_ap'] = None
            post_data['thu_end_hr']   = None
            post_data['thu_end_ap']   = None
        else:
            if post_data['thu_start_ap'] == 0:
                post_data['thu_start_ap'] = 'AM'
            elif post_data['thu_start_ap'] == 1:
                post_data['thu_start_ap'] = 'PM'
            else:
                post_data['thu_start_ap'] = None

            if post_data['thu_end_ap'] == 0:
                post_data['thu_end_ap'] = 'AM'
            elif post_data['thu_end_ap'] == 1:
                post_data['thu_end_ap'] = 'PM'
            else:
                post_data['thu_end_ap'] = None

        if post_data['fri'] == False:
            post_data['fri_start_hr'] = None
            post_data['fri_start_ap'] = None
            post_data['fri_end_hr']   = None
            post_data['fri_end_ap']   = None
        else:
            if post_data['fri_start_ap'] == 0:
                post_data['fri_start_ap'] = 'AM'
            elif post_data['fri_start_ap'] == 1:
                post_data['fri_start_ap'] = 'PM'
            else:
                post_data['fri_start_ap'] = None

            if post_data['fri_end_ap'] == 0:
                post_data['fri_end_ap'] = 'AM'
            elif post_data['fri_end_ap'] == 1:
                post_data['fri_end_ap'] = 'PM'
            else:
                post_data['fri_end_ap'] = None

        if post_data['sat'] == False:
            post_data['sat_start_hr'] = None
            post_data['sat_start_ap'] = None
            post_data['sat_end_hr']   = None
            post_data['sat_end_ap']   = None
        else:
            if post_data['sat_start_ap'] == 0:
                post_data['sat_start_ap'] = 'AM'
            elif post_data['sat_start_ap'] == 1:
                post_data['sat_start_ap'] = 'PM'
            else:
                post_data['sat_start_ap'] = None

            if post_data['sat_end_ap'] == 0:
                post_data['sat_end_ap'] = 'AM'
            elif post_data['sat_end_ap'] == 1:
                post_data['sat_end_ap'] = 'PM'
            else:
                post_data['sat_end_ap'] = None
                
        usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id),data=request.data,context={'request':request})
        if usersr.is_valid():
            usersr.save()
            schedule = Schedule.objects.filter(user=request.user).first()
            if schedule:
                schedulesr = ScheduleSerializer(schedule,data=post_data,context={'request':request})
                if schedulesr.is_valid():
                    schedulesr.save()
            
            categories      = request.data.get('categories')
            subcategories   = request.data.get('subcategories')
            if categories:
                #delete old categries
                deleted = UserCategory.objects.filter(user=request.user).delete()
                for category in categories:
                    if category:
                        cat_user                = UserCategory()
                        cat_user.user           = request.user
                        cat_user.category_id    = category
                        cat_user.save()
                        if subcategories:
                            subs = Subcategory.objects.filter(category_id=category, id__in=subcategories)    
                            if subs:
                                for sub in subs:
                                    if sub:
                                        cat_user.subcategory.add(sub)
            #find latlong
            '''
            address     = str(usersr.instance.address)+','+str(usersr.instance.city.name)+','+str(usersr.instance.zipcode)+' '+str(usersr.instance.state.code)+',USA'
            response    = find_LatLong(address)
            if response['status'] == 'OK':
                result                     = response['results'][0]
                usersr.instance.latitude   = result['geometry']['location']['lat']
                usersr.instance.longitude  = result['geometry']['location']['lng']
            usersr.save()
            '''
            return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
        
        errors = usersr.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

    except Exception as e:

        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

#profile image
@api_view(["POST"])
def contact_details(request):
    try:
        refresh_token(request.user)
        usersr = ContactDetailSerializer(get_user_model().objects.get(id=request.user.id),data=request.data)
        if usersr.is_valid():
            usersr.save()
            usersr.instance.IsProCompleteStatus   = 'Category'
            #find latlong
            address     = str(usersr.instance.address)+','+str(usersr.instance.city.name)+','+str(usersr.instance.zipcode)+' '+str(usersr.instance.state.code)+',USA'
            response    = find_LatLong(address)
            if response['status'] == 'OK':
                result                     = response['results'][0]
                usersr.instance.latitude   = result['geometry']['location']['lat']
                usersr.instance.longitude  = result['geometry']['location']['lng']
            usersr.save()

            usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
            return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
        errors = usersr.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

    except Exception as e:
        db_logger.exception(e)
        print("==============================")
        print(e)
        print("==============================")
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

#profile media
@api_view(["POST"])
def profile_media(request):
    try:
        refresh_token(request.user)
        usersr = ProfileMediaSerializer(get_user_model().objects.get(id=request.user.id),data=request.data)
        if usersr.is_valid():
            usersr.save()
            usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
            return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
        errors = usersr.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

    except Exception as e:
        
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

#change password
@api_view(["POST"])
def change_password(request):
    try:
        refresh_token(request.user)
        changePass = ChangePasswordSerializer(data=request.data,context={'request':request})
        if changePass.is_valid():
            user = request.user
            user.set_password(changePass.validated_data['new_pass'])
            user.save()
            return Response(data={"status":"Success","message":"Password Changed Sucessfully"}, status=HTTP_200_OK)
        
        errors = changePass.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]

        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Change Password Failed"}, status=HTTP_200_OK)

#forgot password request
@api_view(["POST",])
@permission_classes((hasKey,))
def forgot_password_request(request):
    try:
        email = request.data.get('email')
        if not email:
            return Response(data={"status":"Error","message":"Please enter email address"}, status=HTTP_200_OK)
        user = User.objects.filter(email=email, is_active = True, groups__name='Jobseeker').first()
        if user is None:
            return Response(data={"status":"Error","message":"This email address does not exist"}, status=HTTP_200_OK)
        
        #send Temporary Password
        sendTemporaryPassword(request,user)
        
        return Response(data={"status":"Success","message":"Temporary password sent on email address"}, status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"This email address does not exist"}, status=HTTP_400_BAD_REQUEST)

#forgot password reset
@api_view(["POST",])
@permission_classes((hasKey,))
def forgot_password_reset(request):
    try:
        otp                 = request.data.get('otp')
        password            = request.data.get('password')
        password_confirm    = request.data.get('password_confirm')
        email               = request.data.get('email')
        if not otp:
            return Response(data={"status":"Error","message":"Please enter Temporary Password"}, status=HTTP_200_OK)
        if not password:
            return Response(data={"status":"Error","message":"Please enter Password"}, status=HTTP_200_OK)
        if not password_confirm:
            return Response(data={"status":"Error","message":"Please enter Confirm Password"}, status=HTTP_200_OK)
        if password != password_confirm:
            return Response(data={"status":"Error","message":"Password and Confirm Password mismatch"}, status=HTTP_200_OK)
        if not email:
            return Response(data={"status":"Error","message":"Please enter Email Address"}, status=HTTP_200_OK)
        
        user = User.objects.filter(email=email, is_active = True, groups__name='Jobseeker').first()
        if user is None:
            return Response(data={"status":"Error","message":"This email address does not exist"}, status=HTTP_200_OK)

        check_otp = TemporaryPassword.objects.filter(user=user, password = otp, isUsed = False, isExpired = False).first()
        if check_otp is None:
            return Response(data={"status":"Error","message":"Invalid Temporary Password."}, status=HTTP_200_OK)
        
        check_otp.isUsed = True
        check_otp.save()

        #update user
        user.set_password(password)
        user.save()
        
        token, created = Token.objects.get_or_create(user=user)
        if not created:
            utc_now = datetime.datetime.utcnow()
            utc_now = utc_now.replace(tzinfo=pytz.utc)
            token.created = utc_now
            token.save()
        auth_login(request._request, user)
        
        usersr = ProfileSerializer(get_user_model().objects.get(id=user.id))

        return Response(data={"status":"Success","message":"Password changed","token":token.key,"data":usersr.data}, status=HTTP_200_OK)
    
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"This email address does not exist"}, status=HTTP_200_OK)

#profile schedule
@api_view(["POST"])
def profile_schedule(request):
    try:
        refresh_token(request.user)
        post_data = request.data
        if post_data['sun'] == False or  post_data['sun'] == 0:
            post_data['sun_start_hr'] = None
            post_data['sun_start_ap'] = None
            post_data['sun_end_hr']   = None
            post_data['sun_end_ap']   = None
        else:
            if post_data['sun_start_ap'] == 0:
                post_data['sun_start_ap'] = 'AM'
            elif post_data['sun_start_ap'] == 1:
                post_data['sun_start_ap'] = 'PM'
            else:
                post_data['sun_start_ap'] = None

            if post_data['sun_end_ap'] == 0:
                post_data['sun_end_ap'] = 'AM'
            elif post_data['sun_end_ap'] == 1:
                post_data['sun_end_ap'] = 'PM'
            else:
                post_data['sun_end_ap'] = None

        if post_data['mon'] == False:
            post_data['mon_start_hr'] = None
            post_data['mon_start_ap'] = None
            post_data['mon_end_hr']   = None
            post_data['mon_end_ap']   = None
        else:
            if post_data['mon_start_ap'] == 0:
                post_data['mon_start_ap'] = 'AM'
            elif post_data['mon_start_ap'] == 1:
                post_data['mon_start_ap'] = 'PM'
            else:
                post_data['mon_start_ap'] = None

            if post_data['mon_end_ap'] == 0:
                post_data['mon_end_ap'] = 'AM'
            elif post_data['mon_end_ap'] == 1:
                post_data['mon_end_ap'] = 'PM'
            else:
                post_data['mon_end_ap'] = None

        if post_data['tue'] == False:
            post_data['tue_start_hr'] = None
            post_data['tue_start_ap'] = None
            post_data['tue_end_hr']   = None
            post_data['tue_end_ap']   = None
        else:
            if post_data['tue_start_ap'] == 0:
                post_data['tue_start_ap'] = 'AM'
            elif post_data['tue_start_ap'] == 1:
                post_data['tue_start_ap'] = 'PM'
            else:
                post_data['tue_start_ap'] = None

            if post_data['tue_end_ap'] == 0:
                post_data['tue_end_ap'] = 'AM'
            elif post_data['tue_end_ap'] == 1:
                post_data['tue_end_ap'] = 'PM'
            else:
                post_data['tue_end_ap'] = None

        if post_data['wed'] == False:
            post_data['wed_start_hr'] = None
            post_data['wed_start_ap'] = None
            post_data['wed_end_hr']   = None
            post_data['wed_end_ap']   = None
        else:
            if post_data['wed_start_ap'] == 0:
                post_data['wed_start_ap'] = 'AM'
            elif post_data['wed_start_ap'] == 1:
                post_data['wed_start_ap'] = 'PM'
            else:
                post_data['wed_start_ap'] = None

            if post_data['wed_end_ap'] == 0:
                post_data['wed_end_ap'] = 'AM'
            elif post_data['wed_end_ap'] == 1:
                post_data['wed_end_ap'] = 'PM'
            else:
                post_data['wed_end_ap'] = None

        if post_data['thu'] == False:
            post_data['thu_start_hr'] = None
            post_data['thu_start_ap'] = None
            post_data['thu_end_hr']   = None
            post_data['thu_end_ap']   = None
        else:
            if post_data['thu_start_ap'] == 0:
                post_data['thu_start_ap'] = 'AM'
            elif post_data['thu_start_ap'] == 1:
                post_data['thu_start_ap'] = 'PM'
            else:
                post_data['thu_start_ap'] = None

            if post_data['thu_end_ap'] == 0:
                post_data['thu_end_ap'] = 'AM'
            elif post_data['thu_end_ap'] == 1:
                post_data['thu_end_ap'] = 'PM'
            else:
                post_data['thu_end_ap'] = None

        if post_data['fri'] == False:
            post_data['fri_start_hr'] = None
            post_data['fri_start_ap'] = None
            post_data['fri_end_hr']   = None
            post_data['fri_end_ap']   = None
        else:
            if post_data['fri_start_ap'] == 0:
                post_data['fri_start_ap'] = 'AM'
            elif post_data['fri_start_ap'] == 1:
                post_data['fri_start_ap'] = 'PM'
            else:
                post_data['fri_start_ap'] = None

            if post_data['fri_end_ap'] == 0:
                post_data['fri_end_ap'] = 'AM'
            elif post_data['fri_end_ap'] == 1:
                post_data['fri_end_ap'] = 'PM'
            else:
                post_data['fri_end_ap'] = None

        if post_data['sat'] == False:
            post_data['sat_start_hr'] = None
            post_data['sat_start_ap'] = None
            post_data['sat_end_hr']   = None
            post_data['sat_end_ap']   = None
        else:
            if post_data['sat_start_ap'] == 0:
                post_data['sat_start_ap'] = 'AM'
            elif post_data['sat_start_ap'] == 1:
                post_data['sat_start_ap'] = 'PM'
            else:
                post_data['sat_start_ap'] = None

            if post_data['sat_end_ap'] == 0:
                post_data['sat_end_ap'] = 'AM'
            elif post_data['sat_end_ap'] == 1:
                post_data['sat_end_ap'] = 'PM'
            else:
                post_data['sat_end_ap'] = None
        
        schedule = Schedule.objects.filter(user=request.user).first()
        if schedule:
            schedulesr = ScheduleSerializer(schedule,data=post_data,context={'request':request})
        else:
            schedulesr = ScheduleSerializer(data=post_data,context={'request':request})
        if schedulesr.is_valid():
            schedulesr.save()
            schedulesr.instance.source      = request.data.get("source")
            schedulesr.instance.ipaddress   = request.META['REMOTE_ADDR']
            schedulesr.instance.browserinfo = request.META['HTTP_USER_AGENT']
            schedulesr.save()

            user = get_user_model().objects.get(id=request.user.id)
            user.IsProCompleteStatus   = 'Video'
            user.save()

            usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
            return Response(data={"status":"Success","message":"Schedule set","data":usersr.data}, status=HTTP_200_OK)
        
        errors = schedulesr.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

    except Exception as e:

        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

#profile image
@api_view(["POST"])
def profile_image(request):
    try:
        refresh_token(request.user)
        usersr = profileImageSerializer(get_user_model().objects.get(id=request.user.id),data=request.data)
        if usersr.is_valid():
            usersr.save()
            usersr.instance.IsProCompleteStatus   = 'Complete'
            usersr.instance.IsProComplete      = True
            usersr.save()
            usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
            return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
        
        errors = usersr.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

    except Exception as e:

        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

#profile video
@api_view(["POST"])
def profile_video(request):
    try:
        refresh_token(request.user)
        usersr = profileVideoSerializer(get_user_model().objects.get(id=request.user.id),data=request.data)
        if usersr.is_valid():
            usersr.save()
            
            user = get_user_model().objects.get(id=request.user.id)
            user.IsProCompleteStatus   = 'Image'
            user.save()

            usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
            return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
        
        errors = usersr.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

    except Exception as e:

        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

#profile available
@api_view(["POST"])
def profile_available(request):
    try:
        refresh_token(request.user)
        usersr = profileAvailableSerializer(get_user_model().objects.get(id=request.user.id),data=request.data)
        if usersr.is_valid():
            usersr.save()
            usersr = ProfileSerializer(get_user_model().objects.get(id=request.user.id))
            return Response(data={"status":"Success","message":"User Data","data":usersr.data}, status=HTTP_200_OK)
        
        errors = usersr.errors
        errormsg = ''
        for error in errors:
            errormsg += errors[error][0]+'\n\n'
        if errormsg:
            errormsg = errormsg[:-3]
        return Response(data={"status":"Error","message":errormsg}, status=HTTP_200_OK)

    except Exception as e:

        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid user"},status=HTTP_200_OK)

# push notification list
@api_view(["GET",])
def push_notification_list(request):
    try:
        if request.user.is_authenticated:
            refresh_token(request.user)
        records     = Notification.objects.filter(user=request.user, createdAt__gte = datetime.datetime.now()-timedelta(days=7)).order_by('-createdAt')
        if len(records)==0:
            return Response(data={"status":"Error","message":"Notification list not found"},status=HTTP_200_OK)
        respose_list = []
        for record in records:
            respose                 = {}
            respose['message']      = record.message
            respose['datetime']     = record.createdAt.strftime("%d %B, %Y %I:%M %p")
            respose_list.append(respose)
        return Response(data={"status":"Success","message":"Notification list load","data":respose_list},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid request"}, status=HTTP_200_OK)

# push notification
@api_view(["POST",])
def push_notification_update(request):
    try:
        if request.user.is_authenticated:
            refresh_token(request.user)
        device_id    =   request.data.get("device_id")
        source       =   request.data.get("source")
        action       =   request.data.get("action")
        if not device_id:
            return Response(data={"status":"Error","message":"Device ID Required"}, status=HTTP_200_OK)
        if not source:
            return Response(data={"status":"Error","message":"Device Source Required"}, status=HTTP_200_OK)
        if not action:
            return Response(data={"status":"Error","message":"Action Required"}, status=HTTP_200_OK)
        source = source.lower()
        if action == "add":
            devicetoken  =   request.data.get("devicetoken")
            if not devicetoken:
                return Response(data={"status":"Error","message":"Device Token Required"}, status=HTTP_200_OK)
            if devicetoken:
                device = FCMDevice(name=source, user=request.user, device_id=device_id, registration_id=devicetoken, active=True, type=source)
                device.save()
        else:
            device = FCMDevice.objects.filter(user=request.user, device_id=device_id, type=source).first()
            if device:
                device.delete()
        return Response(data={"status":"Success","message":"success"},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid request"}, status=HTTP_200_OK)

# push notification
@api_view(["POST",])
def push_notification_status(request):
    try:
        if request.user.is_authenticated:
            refresh_token(request.user)
        device_id    =   request.data.get("device_id")
        source       =   request.data.get("source")
        if not device_id:
            return Response(data={"status":"Error","message":"Device ID Required"}, status=HTTP_200_OK)
        if not source:
            return Response(data={"status":"Error","message":"Device Source Required"}, status=HTTP_200_OK)
        status = 'off'
        source = source.lower()
        device = FCMDevice.objects.filter(user=request.user, device_id=device_id, type=source).first()
        if device:
            status = 'on'
        return Response(data={"status":"Success","message":"success","push_notification_status":status},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid request"}, status=HTTP_200_OK)

# job offers list
@api_view(["GET",])
def job_offers(request):
    try:
        if request.user.is_authenticated:
            refresh_token(request.user)
        search  = request.query_params.get('search')
        if search:
            records     = JobOffer.objects.filter(user=request.user, job__publish=True).filter(Q(job__title__icontains=search) | Q(job__hiring_company__icontains=search)).order_by('-id')
        else:
            records     = JobOffer.objects.filter(user=request.user, job__publish=True).order_by('-id')
        if len(records)==0:
            return Response(data={"status":"Error","message":"Job Offers list not found"},status=HTTP_200_OK)
        serializer    = JobOffersSerializer(records,many=True)
        return Response(data={"status":"Success","message":"Job Offers load","data":serializer.data},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid request"}, status=HTTP_200_OK)

# job offers list
@api_view(["GET",])
def job_offer_count(request):
    try:
        if request.user.is_authenticated:
            refresh_token(request.user)
        records  = JobOffer.objects.filter(user=request.user, job__publish=True, IsRead = False).count()
        return Response(data={"status":"Success","message":"Job Offers load","data":records},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid request"}, status=HTTP_200_OK)

# job offer details
@api_view(["GET",])
def job_offer_detail(request,token):
    try:
        if request.user.is_authenticated:
            refresh_token(request.user)
        offer           = JobOffer.objects.get(user=request.user, token=token)
        if offer.IsRead == False:
            offer.IsRead            = True
            offer.read_ipaddress    = request.META['REMOTE_ADDR']
            offer.read_browserinfo  = request.META['HTTP_USER_AGENT']
            offer.read_datetime     = datetime.datetime.now()
            offer.read_by           = request.user
            offer.save()
        serializer      = JobOffersSerializer(offer,many=False)
        return Response(data={"status":"Success","message":"Job Offer load","data":serializer.data},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid request"}, status=HTTP_200_OK)

# job offer action
@api_view(["POST",])
def job_offer_action(request,token):
    try:
        if request.user.is_authenticated:
            refresh_token(request.user)
        offer           = JobOffer.objects.get(user=request.user, token=token)
        device_id    =   request.data.get("device_id")
        source       =   request.data.get("source")
        action       =   request.data.get("action")
        if not device_id:
            return Response(data={"status":"Error","message":"Device ID Required"}, status=HTTP_200_OK)
        if not source:
            return Response(data={"status":"Error","message":"Device Source Required"}, status=HTTP_200_OK)
        if not action:
            return Response(data={"status":"Error","message":"Action Required"}, status=HTTP_200_OK)
        if offer.action == 'Pending':
            offer.action = action
            offer.save()
            #offer action
            offer_action              = JobOfferAction()
            offer_action.joboffer     = offer
            offer_action.action       = action
            offer_action.source       = source
            offer_action.ipaddress    = request.META['REMOTE_ADDR']
            offer_action.browserinfo  = request.META['HTTP_USER_AGENT']
            offer_action.createdBy    = request.user
            offer_action.user         = request.user
            offer_action.save()
            #send mail
            send_joboffer_action_email_employer(offer)
            
            serializer      = JobOffersSerializer(JobOffer.objects.get(user=request.user, token=token),many=False)
            return Response(data={"status":"Success","message":"Job Offer load","data":serializer.data},status=HTTP_200_OK)
        else:
            return Response(data={"status":"Error","message":"Request already updated"},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid request"}, status=HTTP_200_OK)

# job offer delete
@api_view(["GET",])
def job_offer_delete(request,token):
    try:
        if request.user.is_authenticated:
            refresh_token(request.user)
        offer = JobOffer.objects.get(user=request.user, token=token)
        offer.delete()
        records       = JobOffer.objects.filter(user=request.user).order_by('-id')
        if len(records)==0:
            return Response(data={"status":"Error","message":"Job Offer has been deleted"},status=HTTP_200_OK)
        serializer    = JobOffersSerializer(records,many=True)
        return Response(data={"status":"Success","message":"Job Offer has been deleted","data":serializer.data},status=HTTP_200_OK)
    except Exception as e:
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Invalid request"}, status=HTTP_200_OK)

#contact us
@api_view(['POST',])
@permission_classes((hasKey,))
def contact_us(request):
    try:
        obj       =   ContactUsSerializer(data=request.data)
        if obj.is_valid():
            obj.save()
            obj.instance.ipaddress   = request.META['REMOTE_ADDR']
            obj.instance.browserinfo = request.META['HTTP_USER_AGENT']
            obj.save()
            
            return Response(data={"status":"Success","message":"Thank you for submitting form."},status=HTTP_200_OK)
        
        errors = obj.errors
        errormsg = ''
        
        for error in errors:
            errormsg += str(error)+' - '+str(errors[error][0])+'\n\n'
        
        if errormsg:
            errormsg = errormsg[:-3] 
        return Response(data={"status":"Error","message":errormsg},status=HTTP_200_OK)
    
    except Exception as e:
        
        db_logger.exception(e)
        return Response(data={"status":"Error","message":"Can't create user"},status=HTTP_400_BAD_REQUEST)

