from django.contrib.auth.decorators import user_passes_test, login_required
from django.http.response import  HttpResponseRedirect
from django.shortcuts import redirect
from accountapp.models import *
from django.conf import settings

#the decorator
def check_role_permission():
    def decorator(f):
        def wrap(request, *args, **kwargs):
                if request.user.is_superuser:
                    return f(request, *args, **kwargs)
                else:
                    role_permission = request.user.groups.filter(name='Employer').exists()
                    if role_permission == False:
                        return HttpResponseRedirect(str(settings.SITE_URL)+"/access-denied")
                    return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
    return decorator

#the decorator
def check_subscription_permission():
    def decorator(f):
        def wrap(request, *args, **kwargs):
                if request.user.is_superuser:
                    return f(request, *args, **kwargs)
                else:
                    subscription = Subscription.objects.filter(user=request.user).last()
                    if subscription:
                        if subscription.expired == True:
                            return HttpResponseRedirect(str(settings.SITE_URL)+"/subscription/expired")
                        if subscription.active == False:
                            return HttpResponseRedirect(str(settings.SITE_URL)+"/subscription/inactive")
                    else:
                        return HttpResponseRedirect(str(settings.SITE_URL)+"/subscription/plan")
                    return f(request, *args, **kwargs)
        wrap.__doc__=f.__doc__
        wrap.__name__=f.__name__
        return wrap
    return decorator