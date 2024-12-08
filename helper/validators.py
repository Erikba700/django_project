from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db import models
from django.shortcuts import redirect


def is_owner_validator(model: type):
    def wrapper(view_func):
        def _wrapped_view_func(request, *args, **kwargs):
            if request.user.profile.is_owner:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request,
                               "You are not allowed to do this action")
                return redirect("pizza:list")

        return _wrapped_view_func
    return wrapper
