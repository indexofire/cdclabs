# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from contrib.form_designer.models import Form, FormSubmission


class FormContent(models.Model):
    """
    It's a content type for feincms.module.page which render basic form
    HTML content in pages.
    Usage:
    Put these lines into anywhere of your app or project which would be
    invoke.
        from feincms.module.page.models import Page
        Page.create_content_type(FormContent)
    """
    FIELD_STYLE_CHOICES = (
        ('jqtransform', 'jqtransformplugin'),
    )
    form = models.ForeignKey(Form, verbose_name=_('form'),
        related_name='%(app_label)s_%(class)s_related',)
    show_form_title = models.BooleanField(_('show form title'),
        default=True,)
    success_message = models.TextField(_('success message'),
        blank=True, help_text=_("Optional custom message to display "
        "after valid form is submitted"),)
    template = 'form/form.html'
    #form_style = models.CharField(choices=FIELD_STYLE_CHOICES,)
    
    class Meta:
        abstract = True
        verbose_name = _('form content')
        verbose_name_plural = _('form contents')

    @property
    def media(self):
        return forms.Media(
            css={'all': ('js/jqtransformplugin/jqtransform.css',)},
            js=('js/jqtransformplugin/jquery.jqtransform.js',)
            )

    def process_valid_form(self, request, form_instance, **kwargs):
        """
        Process form and return response (hook method).
        """
        process_result = self.form.process(form_instance, request)
        context = RequestContext(request, {
            'content': self,
            'message': self.success_message or process_result or u'',
            })
        return render_to_string(self.template, context)

    def render(self, request, **kwargs):
        """
        Process form content block render
        """
        form_class = self.form.form()
        prefix = 'fc%d' % self.id

        if request.method == 'POST':
            form_instance = form_class(request.POST, prefix=prefix)
            if form_instance.is_valid():
                return self.process_valid_form(request, form_instance,
                    **kwargs)
        else:
            form_instance = form_class(prefix=prefix)
            try:
                form_submission_object = FormSubmission.objects.get(
                    path=request.path)
                if form_submission_object.sorted_data()['submitter'] == str(request.user):
                    context = RequestContext(request, {
                        'content': self,
                        'info': '你已提交结果数据，如果需要修改请联系杭州疾控中心-汪皓秋',
                        'form': form_submission_object.formatted_data_html(),
                        'is_submitter': 0,
                        })
                    return render_to_string(self.template, context)
                else:
                    context = RequestContext(request, {
                        'content': self,
                        'form': form_instance,
                        'is_submitter': 1,
                        })
                    return render_to_string(self.template, context)
            except:
                context = RequestContext(request, {
                    'content': self,
                    'form': form_instance,
                    })
                return render_to_string(self.template, context)

        #fs_object = get_object_or_404(FormSubmission, path=request.path)
        #if fs_object.sorted_data()['submitter'] == str(request.user):
        #    context = RequestContext(request, {
        #    'content': self,
        #    'form': 'you have finished the form',
        #    })
        #    return render_to_string(self.template, context)
        #form_class = self.form.form()
        #prefix = 'fc%d' % self.id

        #if request.method == 'POST':
        #    form_instance = form_class(request.POST, prefix=prefix)
        #    if form_instance.is_valid():
        #        return self.process_valid_form(request, form_instance, **kwargs)
        #else:
        #    form_instance = form_class(prefix=prefix)
        #context = RequestContext(request, {
        #    'content': self,
        #    'form': form_instance,
        #    })
        #return render_to_string(self.template, context)
