from rest_framework import serializers, permissions
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from accountapp.models import *
from jobapp.models import *
from backendapp.humanizedatetime import time_ago
from datetime import datetime
from django.conf import settings
import os

class CurrentUser(object):
    def set_context(self, serializer_field):
        self.user_obj = serializer_field.context['request'].user
    def __call__(self):
        return self.user_obj

#user change password serializer
class ChangePasswordSerializer(serializers.Serializer):
    old_pass        = serializers.CharField()
    new_pass        = serializers.CharField()
    confirm_pass    = serializers.CharField()

    def validate(self, data):
        if data['new_pass']!=data['confirm_pass']:
            raise serializers.ValidationError("Confirm password does not match")
        elif data['new_pass']==data['old_pass']:
            raise serializers.ValidationError("New password can not be same as old password")
        return data

    def validate_new_pass(self, new_pass):
        user = self.context['request'].user
        validate_password(new_pass, user=user)
        return new_pass

    def validate_old_pass(self, old_pass):
        user = self.context['request'].user
        if not user.check_password(old_pass):
            raise serializers.ValidationError("Old password does not match")
        return old_pass

#State model serializer
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ("id", "name","code")

#City model serializer
class CitySerializer(serializers.ModelSerializer):
    state_name = serializers.ReadOnlyField(source='state.name', read_only=True)
    class Meta:
        model = City
        fields = ("id","name","state_name")
        read_only_fields = ("id","state_name")

#Category model serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")

#Sub Category model serializer
class SubCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name', read_only=True)
    class Meta:
        model = Subcategory
        fields = ("id","name","category_name")
        read_only_fields = ("id","category_name")

#Language model serializer
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("id", "name","code")

#Schedule model serializer
class ScheduleSerializer(serializers.ModelSerializer):

    user            = serializers.HiddenField(default=serializers.CurrentUserDefault())
    createdBy       = serializers.HiddenField(default=serializers.CurrentUserDefault())
    pf_time_lable   = serializers.SerializerMethodField(read_only=True)
    
    def get_pf_time_lable(self, obj):
        if obj.part_time and obj.full_time:
            return 'Part Time, Full Time'
        elif obj.part_time:
            return 'Part Time'
        elif obj.full_time:
            return 'Full Time'
        else:
            return ''
    
    class Meta:
        model = Schedule
        fields = ("user", "createdBy", "part_time","full_time","pf_time_lable",
                    'sun','sun_start_hr','sun_start_ap','sun_end_hr','sun_end_ap',
                    'mon','mon_start_hr','mon_start_ap','mon_end_hr','mon_end_ap',
                    'tue','tue_start_hr','tue_start_ap','tue_end_hr','tue_end_ap',
                    'wed','wed_start_hr','wed_start_ap','wed_end_hr','wed_end_ap',
                    'thu','thu_start_hr','thu_start_ap','thu_end_hr','thu_end_ap',
                    'fri','fri_start_hr','fri_start_ap','fri_end_hr','fri_end_ap',
                    'sat','sat_start_hr','sat_start_ap','sat_end_hr','sat_end_ap')
        read_only_fields = ("pf_time_lable",)

    def create(self, validated_data):
        sch=super(ScheduleSerializer,self).create(validated_data)
        sch.save()
        return sch

#user create serializer
class UserSerializer(serializers.ModelSerializer):
    password    = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2   = serializers.CharField(write_only=True, required=True)

    class Meta:
        model= get_user_model()
        fields=("first_name","last_name","email","password","password2")
        #read_only_fields = ("state_name","city_name")
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_password(self, password):
        validate_password(password)
        return password

    def create(self, validated_data):
        user = User.objects.create(
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        email=validated_data['email'])
        user.set_password(validated_data['password'])
        #save user group
        group = Group.objects.get(name='Jobseeker')
        user.groups.add(group)
        user.save()
        return user

#User Register Serializer Step2
class ContactDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= get_user_model()
        # fields=("address","zipcode","state","city","mobile","yourself","employee_type","price","availbility","authorized_to_work_in_us","is_us_veteran","years_served","distance_willing_to_travel","bilingual","transportation")
        fields=("address","zipcode","state","city","mobile","yourself")
        extra_kwargs = {
            'address': {'required': True},
            'zipcode': {'required': True},
            # 'state': {'required': True},
            # 'city': {'required': True},
            'state': {'required': False},
            'city': {'required': False},
            'mobile': {'required': True},
            'yourself': {'required': True},
            # New
            # 'employee_type': {'required': True},
            # 'price': {'required': True},
            # 'availbility': {'required': True},
            # 'authorized_to_work_in_us': {'required': True},
            # 'is_us_veteran': {'required': True},
            # 'years_served': {'required': True},
            # 'distance_willing_to_travel': {'required': True},
            # 'bilingual': {'required': True},
            # 'transportation': {'required': True},



            }
    
    def update(self, instance, validated_data):
        instance.address    = validated_data.get('address', instance.address)
        instance.zipcode    = validated_data.get('zipcode', instance.zipcode)
        instance.state      = validated_data.get('state', instance.state)
        instance.city       = validated_data.get('city', instance.city)
        instance.mobile     = validated_data.get('mobile', instance.mobile)
        instance.yourself   = validated_data.get('yourself', instance.yourself)
        # New
        # instance.employee_type       = validated_data.get('employee_type', instance.employee_type)
        # instance.price               = validated_data.get('price', instance.price)
        # instance.availbility         = validated_data.get('availbility', instance.availbility)
        # instance.authorized_to_work_in_us       = validated_data.get('authorized_to_work_in_us', instance.authorized_to_work_in_us)
        # instance.is_us_veteran       = validated_data.get('is_us_veteran', instance.is_us_veteran)
        # instance.years_served        = validated_data.get('years_served', instance.years_served)
        # instance.distance_willing_to_travel     = validated_data.get('distance_willing_to_travel', instance.distance_willing_to_travel)
        # instance.bilingual           = validated_data.get('bilingual', instance.bilingual)
        # instance.transportation      = validated_data.get('transportation', instance.transportation)
        instance.save()
        return instance

#User Register Serializer Step2
class profileYourselfSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= get_user_model()
        fields=("yourself",)
        extra_kwargs = {'yourself': {'required': True}}
    
    def update(self, instance, validated_data):
        instance.yourself   = validated_data.get('yourself', instance.yourself)
        instance.save()
        return instance

#User Profile Image
class profileImageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= get_user_model()
        fields=("image",)
        extra_kwargs = {
            'image': {'required': True}
            }
    
    def update(self, instance, validated_data):
        instance.image   = validated_data.get('image', instance.image)
        instance.save()
        return instance

#User Profile Video
class profileVideoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= get_user_model()
        fields=("video",)
        extra_kwargs = {'video': {'required': True}}
    
    def update(self, instance, validated_data):
        instance.video      = validated_data.get('video', instance.video)
        instance.save()
        return instance

#User Profile Video
class profileAvailableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= get_user_model()
        fields=("available",)
        extra_kwargs = {
            'available': {'required': True}
            }
    
    def update(self, instance, validated_data):
        instance.available   = validated_data.get('available', instance.available)
        instance.save()
        return instance

#user update serializer
class ProfileSerializer(serializers.ModelSerializer):
    state_name          = serializers.ReadOnlyField(source='state.name', read_only=True)
    city_name           = serializers.ReadOnlyField(source='city.name', read_only=True)
    image_url           = serializers.SerializerMethodField(read_only=True)
    video_url           = serializers.SerializerMethodField(read_only=True)
    
    def get_image_url(self, user):
        if user.image:
            return str(settings.SITE_URL)+str(user.image.url)
        else:
            return ''
    
    def get_video_url(self, user):
        if user.video:
            basename = os.path.basename(user.video.url)
            return 'http://157.230.95.3:9000/'+str(basename)
            #return 'https://gtwa.notionmind.com'+str(user.video.url)
            #return str(settings.SITE_URL)+str(user.video.url)
            #return 'https://flutter.github.io/assets-for-api-docs/assets/videos/butterfly.mp4'
        else:
            return ''

    class Meta:
        model= get_user_model()
        fields=("first_name","last_name","address","zipcode","state","city","mobile","email","state_name","city_name","yourself","available","image","video","image_url","video_url","IsProComplete","IsProCompleteStatus")
        read_only_fields = ('id',"state_name","city_name","image_url","video_url")
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'mobile': {'required': True},
            'email': {'required': True},
            'address': {'required': True},
            'zipcode': {'required': True},
            'state': {'required': True},
            'city': {'required': True},
            'mobile': {'required': True}
        }
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["language"] = LanguageSerializer(instance.language.all(), many=True).data
        rep["schedule"] = ScheduleSerializer(Schedule.objects.filter(user=instance).first(), many=False).data
        categories      = UserCategory.objects.filter(user=instance)
        categories_list = []
        if  categories :
            for category in categories:
                cat_res             = {}
                cat_res['id']       = category.category.id
                cat_res['name']     = category.category.name
                subcategories_list   = []
                subs                 = category.subcategory.all()
                if subs:
                    for sub in subs:
                        sub_respose = {}
                        sub_respose['id']        = sub.id
                        sub_respose['name']      = sub.name
                        subcategories_list.append(sub_respose)
                cat_res['subcategories']  = subcategories_list
                categories_list.append(cat_res)
        rep["categories"] = categories_list
        return rep

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name  = validated_data.get('last_name', instance.last_name)
        instance.address    = validated_data.get('address', instance.address)
        instance.zipcode    = validated_data.get('zipcode', instance.zipcode)
        instance.state      = validated_data.get('state', instance.state)
        instance.city       = validated_data.get('city', instance.city)
        instance.mobile     = validated_data.get('mobile', instance.mobile)
        instance.email      = validated_data.get('email', instance.email)
        instance.yourself   = validated_data.get('yourself', instance.yourself)
        instance.image      = validated_data.get('image', instance.image)
        instance.video      = validated_data.get('video', instance.video)
        instance.available  = validated_data.get('available', instance.available)
        instance.save()
        return instance

#user media update serializer
class ProfileMediaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model= get_user_model()
        fields=("image","video")
        
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        return rep

    def update(self, instance, validated_data):
        instance.image      = validated_data.get('image', instance.image)
        instance.video      = validated_data.get('video', instance.video)
        instance.save()
        return instance

#Job Schedule model serializer
class JobScheduleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = JobShiftSchedule
        fields = ('sun',"startdate","enddate",'sun_start_hr','sun_start_ap','sun_end_hr','sun_end_ap',
                    'mon','mon_start_hr','mon_start_ap','mon_end_hr','mon_end_ap',
                    'tue','tue_start_hr','tue_start_ap','tue_end_hr','tue_end_ap',
                    'wed','wed_start_hr','wed_start_ap','wed_end_hr','wed_end_ap',
                    'thu','thu_start_hr','thu_start_ap','thu_end_hr','thu_end_ap',
                    'fri','fri_start_hr','fri_start_ap','fri_end_hr','fri_end_ap',
                    'sat','sat_start_hr','sat_start_ap','sat_end_hr','sat_end_ap')

#user job offers serializer
class JobSerializer(serializers.ModelSerializer):

    state_name          = serializers.ReadOnlyField(source='state.name', read_only=True)
    city_name           = serializers.ReadOnlyField(source='city.name', read_only=True)
    category_name       = serializers.ReadOnlyField(source='category.name', read_only=True)
    image_url           = serializers.SerializerMethodField(read_only=True)
    
    def get_image_url(self, obj):
        if obj.user.image:
            return str(settings.SITE_URL)+str(obj.user.image.url)
        else:
            return ''
    
    class Meta:
        model   =   Job 
        fields  =   ("title","description","detail","hourly_rate","hiring_manager_name","hiring_company","email","phone","state_name","city_name","address","zipcode","latitude","longitude","category_name","image_url")
        read_only_fields = ('id',"state_name","city_name","category_name","image_url")

    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        schedule =  JobScheduleSerializer(JobShiftSchedule.objects.filter(job=instance).first(), many=False).data
        if schedule:
            if schedule['startdate']:
                startdate               = schedule['startdate']
                startdate               = datetime.strptime(startdate, '%Y-%m-%d')
                schedule['startdate']   = startdate.strftime('%m-%d-%Y')
            if schedule['enddate']:
                enddate                 = schedule['enddate']
                enddate                 = datetime.strptime(enddate, '%Y-%m-%d')
                schedule['enddate']     = enddate.strftime('%m-%d-%Y')
        rep["schedule"]     = schedule
        rep["subcategory"]  = SubCategorySerializer(instance.subcategory.all(), many=True).data
        return rep
    
#user job offers serializer
class JobOffersSerializer(serializers.ModelSerializer):

    company     = serializers.ReadOnlyField(source='job.hiring_company', read_only=True)
    job_title   = serializers.ReadOnlyField(source='job.title', read_only=True)
    job_rate    = serializers.ReadOnlyField(source='job.hourly_rate', read_only=True)
    job_desc    = serializers.ReadOnlyField(source='job.description', read_only=True)
    status      = serializers.SerializerMethodField(read_only=True)
    action_date = serializers.SerializerMethodField(read_only=True)
    created     = serializers.SerializerMethodField(read_only=True)
    image_url   = serializers.SerializerMethodField(read_only=True)
    note        = serializers.SerializerMethodField(read_only=True)
    
    def get_image_url(self, obj):
        if obj.job.user.image:
            return str(settings.SITE_URL)+str(obj.job.user.image.url)
        else:
            return ''
    
    def get_status(self, obj):
        if obj.IsRead:
            return 'Seen'
        else:
            return 'Unread'
    
    def get_action_date(self, obj):
        offer_action = JobOfferAction.objects.filter(joboffer=obj).last()
        if offer_action:
            return time_ago(offer_action.createdAt)
        else:    
            return 'N/A'
    
    def get_created(self, obj):
        return time_ago(obj.createdAt)
    
    def get_note(self, obj):
        if obj.action == 'Accept':
            return "You've been accepted for "+str(obj.job.title)+" as "+str(obj.job.hiring_company)+" for $"+str(obj.job.hourly_rate)+"/hr."
        else:
            return ''
        
    class Meta:
        model               =   JobOffer 
        fields              =   ("token","company","job_title","job_rate","job_desc","status","IsRead","action","action_date","created","image_url","note")
        read_only_fields    =   ('id',"company","job_title","job_rate","job_desc","status","action_date","created","image_url","note")
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["job_info"] = JobSerializer(Job.objects.filter(id=instance.job.id).first(), many=False).data
        return rep

#user job offers serializer
class ContactUsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model   =   ContactUs 
        fields  =   ("name","email","phone","message","source")
    