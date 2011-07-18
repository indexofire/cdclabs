# -*- coding: utf-8 -*-
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from contrib.form_designer.models import Form


class FormContent(models.Model):
    form = models.ForeignKey(Form, verbose_name=_('form'),
                             related_name='%(app_label)s_%(class)s_related')
    show_form_title = models.BooleanField(_('show form title'), default=True)
    success_message = models.TextField(
        _('success message'), blank=True, help_text=
        _("Optional custom message to display after valid form is submitted"))

    template = 'content/form/form.html'

    class Meta:
        abstract = True
        verbose_name = _('form content')
        verbose_name_plural = _('form contents')

    def process_valid_form(self, request, form_instance, **kwargs):
        """ Process form and return response (hook method). """
        process_result = self.form.process(form_instance, request)
        context = RequestContext(
            request, {
                'content': self,
                'message': self.success_message or process_result or u''})
        return render_to_string(self.template, context)

    def render(self, request, **kwargs):
        form_class = self.form.form()
        prefix = 'fc%d' % self.id

        if request.method == 'POST':
            form_instance = form_class(request.POST, prefix=prefix)

            if form_instance.is_valid():
                return self.process_valid_form(request, form_instance, **kwargs)
        else:
            form_instance = form_class(prefix=prefix)

        context = RequestContext(
            request, {'content': self, 'form': form_instance})
        return render_to_string(self.template, context)
