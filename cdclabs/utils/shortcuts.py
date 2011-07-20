# -*- coding: utf-8 -*-
import os.path
import hashlib
import datetime
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.http import HttpResponseRedirect


def build_filename(instance, filename):
    """
    Converts an image filename to a hash.
    """
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    name = hashlib.md5('%s' % now).hexdigest()
    ext = os.path.splitext(filename)
    return os.path.join('%s/%s' % (instance._meta.app_label, instance._meta.module_name), '%s%s' % (name, ext[1]))


def render(request, *args, **kwargs):
    """
    Simple wrapper for render_to_response.
    """
    kwargs['context_instance'] = RequestContext(request)
    return render_to_response(*args, **kwargs)


def redirect(request, obj=None):
    """
    Simple wrapper for HttpResponseRedirect that checks the request for a
    'next' GET parameter then falls back to a given object or url string.
    """
    next = request.GET.get('next', None)
    redirect_url = '/'

    if next:
        redirect_url = next
    elif isinstance(obj, str):
        redirect_url = obj
    elif obj and hasattr(obj, 'get_absolute_url'):
        redirect_url = obj.get_absolute_url()
    return HttpResponseRedirect(redirect_url)


def request_get_next(request):
    """
    The part that's the least straightforward about views in this module
    is how they determine their redirects after they have finished
    computation.

    In short, they will try and determine the next place to go in the
    following order:
    1. If there is a variable named ``next`` in the *POST* parameters,
    the view will redirect to that variable's value.
    2. If there is a variable named ``next`` in the *GET* parameters,
    the view will redirect to that variable's value.
    3. If Django can determine the previous page from the HTTP headers,
    the view will redirect to that previous page.
    """
    next = request.POST.get('next', request.GET.get('next',
        request.META.get('HTTP_REFERER', None)))
    if not next:
        next = request.path
    return next
