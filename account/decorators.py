from django.http import HttpResponse
from django.shortcuts import render, redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            if request.user.get_group() == 'user':
                return redirect('u_dashboard')
            elif request.user.get_group() == 'admin' or request.user.get_group() == 'subadmin':
                return redirect('a_dashboard')
    return wrapper_func


def allowed_roles(roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = request.user.get_group()

            if group in roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator
