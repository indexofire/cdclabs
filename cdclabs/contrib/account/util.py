# -*- coding: utf-8 -*-
import re
import os.path
import logging
from datetime import datetime
from django.conf import settings
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.shortcuts import render_to_response
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.models import Site
from django.template import TemplateDoesNotExist
from django.core.mail import EmailMultiAlternatives


def build_redirect_url(request, default_url):
    """
    Retrieve redirect url from session.

    Use default if retrieved one is broken or not safe.
    """

    url = request.session.get('login_redirect_url')
    if not url or '//' in url or ' ' in url:
        url = default_url
    try:
        del request.session['login_redirect_url']
    except KeyError:
        pass
    return url


def parse_template(template_path, **kwargs):
    """
    Load and render template.

    First line of template should contain the subject of email.
    Return tuple with subject and content.
    """

    template = get_template(template_path)
    context = Context(kwargs)
    re_empty_lines = re.compile(r'^(\r?\n)+|(\r?\n)+$')
    data = template.render(context)
    return re_empty_lines.sub('', data)


def email_template(rcpt, template_path, **kwargs):
    """
    Load, render and email template.

    Template_path should not contain .txt or .html suffixes - they
    will be appended automatically.

    **kwargs may contain variables for template rendering.
    """

    from_email = settings.DEFAULT_FROM_EMAIL

    subject = parse_template('%s_subject.txt' % template_path, **kwargs)
    text_content = parse_template('%s_body.txt' % template_path, **kwargs)

    try:
        html_content = parse_template('%s_body.html' % template_path, **kwargs)
    except TemplateDoesNotExist:
        html_content = None

    # TODO remove after debugging
    # print text_content

    msg = EmailMultiAlternatives(subject, text_content, from_email, [rcpt])
    if html_content:
        msg.attach_alternative(html_content, "text/html")

    return bool(msg.send(fail_silently=True))


def render_to(template_path):
    """
    Decorate the django view.

    Wrap view that return dict of variables, that should be used for
    rendering the template.
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            output = func(request, *args, **kwargs)
            if not isinstance(output, dict):
                return output
            ctx = RequestContext(request)
            return render_to_response(template_path, output,
                                      context_instance=ctx)
        return wrapper
    return decorator


def load_class(path):
    from django.db.models.loading import get_app
    module_path, class_name = path.rsplit('.', 1)
    mod = __import__(module_path, globals(), locals(), ['foobar'])
    return getattr(mod, class_name)


def build_absolute_url(url):
    return 'http://%s%s' % (Site.objects.get_current().domain, url)
