from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapper_func(requests, *args, **kwargs):
        if requests.user.is_authenticated:
            return redirect('/')
        return view_func(requests, *args, **kwargs)

    return wrapper_func

def allowed_user(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func( requests, *args, **kwargs ):
            group=None
            if requests.user.groups.exists():
                group=requests.user.groups.all()[0]
                print(group)
            print(group)
            print(allowed_roles)
            if str(group) in allowed_roles:
                print('yessss')
                return view_func(requests, *args, **kwargs)
            else:
                return HttpResponse('you are not authorized to view this page')
            return view_func(requests, *args, **kwargs)
        return wrapper_func
    return decorator