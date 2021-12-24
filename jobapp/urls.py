from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('listing', views.job_list,name='job_list'),
    path('status', views.job_status, name='job_status'),
    path('create', views.job_create, name='job_create'),
    path('offers', views.job_offers, name='job_offers'),
    path('offers/edit/<str:token>', views.job_offers_edit, name='job_offers_edit'),
    path('offers/view/<str:token>', views.job_offers_view, name='job_offers_view'),
    path('offers/payroll-service/<str:token>', views.job_offers_payroll_service, name='job_offers_payroll_service'),
    path('view/<str:token>', views.job_view, name='job_view'),
    path('edit/<str:token>', views.job_update, name='job_edit'),
    path('delete/<str:token>', views.job_delete, name='job_delete'),
    path('schedule/<str:token>', views.job_schedule, name='job_schedule'),
]