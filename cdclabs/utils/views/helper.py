# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response


def render_to(template_path):
    """
    Decorate the django view.

    Wrap view that return dict of variables, that should be used for
    rendering the template.

    Usage:
    @render_to('apps/template_name.html')
    def your_custom_views(request):
        view code...
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict): return output
            ctx = RequestContext(request)
            return render_to_response(template_path, output,
                context_instance=ctx)
        return wrapper
    return decorator
