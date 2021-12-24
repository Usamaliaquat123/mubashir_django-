from django.urls import path, include
from django.conf.urls import url
from . import views, employer, jobseeker, category, subcategory, state, city, language, plan, subscription, job, apikey, blog, blogcategory, contactus

urlpatterns = [
    path('', views.login_view,name='backend_login'),
    path('login', views.login_view,name='backend_login'),
    path('logout', views.logout_view, name='backend_logout'),
    path('dashboard', views.dashboard,name='backend_dashboard'),
    path('profile', views.profile,name='backend_profile'),
    path('change-password', views.change_password,name='backend_change_password'),
    path('cities/<int:pk>', views.cities, name='backend_cities_list'), #get cities list
    path('subcategories/<int:pk>', views.subcategories, name='backend_subcategories_list'), #get subcategories list
    #category management
    path('category/listing', category.category_list, name='backend_category_list'),
    path('category/status', category.category_status, name='backend_category_status'),
    path('category/new', category.category_create, name='backend_category_new'),
    path('category/edit/<str:token>', category.category_update, name='backend_category_edit'),
    path('category/delete/<str:token>', category.category_delete, name='backend_category_delete'),
    #subcategory management
    path('subcategory/listing', subcategory.subcategory_list, name='backend_subcategory_list'),
    path('subcategory/status', subcategory.subcategory_status, name='backend_subcategory_status'),
    path('subcategory/new', subcategory.subcategory_create, name='backend_subcategory_new'),
    path('subcategory/edit/<str:token>', subcategory.subcategory_update, name='backend_subcategory_edit'),
    path('subcategory/delete/<str:token>', subcategory.subcategory_delete, name='backend_subcategory_delete'),
    #state management
    path('state/listing', state.state_list, name='backend_state_list'),
    path('state/status', state.state_status, name='backend_state_status'),
    path('state/new', state.state_create, name='backend_state_new'),
    path('state/edit/<str:token>', state.state_update, name='backend_state_edit'),
    path('state/delete/<str:token>', state.state_delete, name='backend_state_delete'),
    #city management
    path('city/listing', city.city_list, name='backend_city_list'),
    path('city/status', city.city_status, name='backend_city_status'),
    path('city/new', city.city_create, name='backend_city_new'),
    path('city/edit/<str:token>', city.city_update, name='backend_city_edit'),
    path('city/delete/<str:token>', city.city_delete, name='backend_city_delete'),
    #language management
    path('language/listing', language.language_list, name='backend_language_list'),
    path('language/status', language.language_status, name='backend_language_status'),
    path('language/new', language.language_create, name='backend_language_new'),
    path('language/edit/<str:token>', language.language_update, name='backend_language_edit'),
    path('language/delete/<str:token>', language.language_delete, name='backend_language_delete'),
    #employer management    
    path('employer/listing', employer.employer_list, name='backend_employer_list'),
    path('employer/status', employer.employer_status, name='backend_employer_status'),
    path('employer/view/<str:token>', employer.employer_view, name='backend_employer_view'),
    path('employer/new', employer.employer_create, name='backend_employer_new'),
    path('employer/edit/<str:token>', employer.employer_update, name='backend_employer_edit'),
    path('employer/delete/<str:token>', employer.employer_delete, name='backend_employer_delete'),
    path('employer/change-password/<str:token>', employer.employer_change_password, name='backend_employer_change_password'),
    #Jobseeker management
    path('jobseeker/listing', jobseeker.jobseeker_list, name='backend_jobseeker_list'),
    path('jobseeker/status', jobseeker.jobseeker_status, name='backend_jobseeker_status'),
    path('jobseeker/view/<str:token>', jobseeker.jobseeker_view, name='backend_jobseeker_view'),
    path('jobseeker/new', jobseeker.jobseeker_create, name='backend_jobseeker_new'),
    path('jobseeker/edit/<str:token>', jobseeker.jobseeker_update, name='backend_jobseeker_edit'),
    path('jobseeker/delete/<str:token>', jobseeker.jobseeker_delete, name='backend_jobseeker_delete'),
    path('jobseeker/change-password/<str:token>', jobseeker.jobseeker_change_password, name='backend_jobseeker_change_password'),
    path('jobseeker/schedule/<str:token>', jobseeker.jobseeker_schedule, name='backend_jobseeker_schedule'),
    #plan management
    path('plan/listing', plan.plan_list, name='backend_plan_list'),
    path('plan/status', plan.plan_status, name='backend_plan_status'),
    path('plan/new', plan.plan_create, name='backend_plan_new'),
    path('plan/edit/<str:token>', plan.plan_update, name='backend_plan_edit'),
    path('plan/detail/<str:token>', plan.plan_detail, name='backend_plan_detail'),
    path('plan/delete/<str:token>', plan.plan_delete, name='backend_plan_delete'),
    #subscription management
    path('subscription/listing', subscription.subscription_list, name='backend_subscription_list'),
    path('subscription/status', subscription.subscription_status, name='backend_subscription_status'),
    path('subscription/new', subscription.subscription_create, name='backend_subscription_new'),
    path('subscription/view/<str:token>', subscription.subscription_view, name='backend_subscription_view'),
    #job management    
    path('job/listing', job.job_list, name='backend_job_list'),
    path('job/status', job.job_status, name='backend_job_status'),
    path('job/view/<str:token>', job.job_view, name='backend_job_view'),
    path('job/new', job.job_create, name='backend_job_new'),
    path('job/edit/<str:token>', job.job_update, name='backend_job_edit'),
    path('job/delete/<str:token>', job.job_delete, name='backend_job_delete'),
    path('job/schedule/<str:token>', job.job_schedule, name='backend_job_schedule'),
    path('job/jobseeker/<str:token>', job.jobseeker_list, name='backend_job_jobseeker_list'),
    path('job/jobseeker/send-request/<str:token>', job.jobseeker_send_request, name='backend_job_jobseeker_send_request'),
    #API KEYS
    path('apikey/listing', apikey.apikey_list, name='backend_apikey_list'),
    path('apikey/status', apikey.apikey_status, name='backend_apikey_status'),
    path('apikey/generate', apikey.apikey_generate, name='backend_apikey_generate'),

    #blog management
    path('blog/category/listing', blogcategory.category_list, name='backend_blogcategory_list'),
    path('blog/category/status', blogcategory.category_status, name='backend_blogcategory_status'),
    path('blog/category/new', blogcategory.category_create, name='backend_blogcategory_new'),
    path('blog/category/edit/<int:pk>', blogcategory.category_update, name='backend_blogcategory_edit'),
    path('blog/category/delete/<int:pk>', blogcategory.category_delete, name='backend_blogcategory_delete'),
    path('blog/listing', blog.blog_list, name='backend_blog_list'),
    path('blog/status', blog.blog_status, name='backend_blog_status'),
    path('blog/view/<str:token>', blog.blog_view, name='backend_blog_view'),
    path('blog/new', blog.blog_create, name='backend_blog_new'),
    path('blog/edit/<str:token>', blog.blog_update, name='backend_blog_edit'),
    path('blog/delete/<str:token>', blog.blog_delete, name='backend_blog_delete'),
    path('blog/comment/delete/<str:token>/<int:pk>', blog.blog_comment_delete, name='backend_blog_comment_delete'),

    #contct us management
    path('contactus/listing', contactus.contactus_list, name='backend_contactus_list'),
    path('contactus/view/<int:pk>', contactus.contactus_view, name='backend_contactus_view'),
    path('contactus/delete/<int:pk>', contactus.contactus_delete, name='backend_contactus_delete'),
] 