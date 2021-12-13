from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('how-it-works', views.how_it_works,name='how_it_works'),
    path('sign-in', views.sign_in,name='sign_in'),
    path('sign-out', views.sign_out, name='sign_out'),
    path('sign-up', views.sign_up,name='sign_up'),
    path('password_reset', views.password_reset,name='password_reset'),
    url(r'^password_reset/done/$', views.password_reset_done, name='password_reset_done'),
    #url(r'^reset/(?P<uid>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/<str:uid>/<str:token>/', views.password_reset_confirm,name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    path('dashboard', views.dashboard,name='dashboard'),
    path('profile', views.profile,name='profile'),
    path('change-password', views.change_password,name='change_password'),
    path('allow-location/<str:latitude>/<str:longitude>', views.allow_location,name='allow_location'),
    path('denied-location', views.denied_location,name='denied_location'),
    path('cities/<int:pk>', views.cities, name='cities_list'), #get cities list
    path('subcategories/<int:pk>', views.subcategories, name='subcategories_list'), #get subcategories list
    path('find-job-seekers', views.find_job_seekers,name='find_job_seekers'),
    path('job-seeker/<str:token>', views.job_seeker_profile,name='job_seeker_profile'),
    path('access-denied', views.access_denied,name='access_denied'),
    path('contact-us', views.contact_us,name='contact_us'),
    path('subscription', views.subscription,name='subscription'),
    path('subscription/plan', views.subscription_plan,name='subscription_plan'),
    path('subscription/expired', views.subscription_expired,name='subscription_expired'),
    path('subscription/inactive', views.subscription_inactive,name='subscription_inactive'),
    path('subscription/cancel', views.subscription_cancel,name='subscription_cancel'),
    path('subscription/<str:plan>/checkout', views.subscription_checkout,name='subscription_checkout'),
    path('subscription/success/<str:plan>', views.subscription_success,name='subscription_success'),
    path('subscription/back/<str:plan>', views.subscription_back,name='subscription_back'),
    path('webhooks/stripe/', views.stripe_webhook,name='stripe_webhook'),
    path('language/<str:lang>', views.language,name='language'),
    path('newsletter-subscription', views.newsletter_subscription,name='newsletter_subscription'),
]