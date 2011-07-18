# -*- coding: utf-8 -*-
import re

from django import template

from account.forms import LoginForm


register = template.Library()

@register.tag(name='get_login_form')
def do_get_login_form(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]

    match = re.search(r'as\s+(\w+)', arg)
    if not match:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    name = match.group(1)

    return GetLoginFormNode(name)


class GetLoginFormNode(template.Node):
    def __init__(self, name):
        self.name = name

    def render(self, context):
        context[self.name] = LoginForm(request=context['request'])
        return ''
