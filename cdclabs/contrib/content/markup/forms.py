# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from feincms.admin.editor import ItemEditorForm
from contrib.content.markup.widgets import MarkItUpWidget


class MarkupContentAdminForm(ItemEditorForm):
    """
    Admin Form to use markitup editor
    """
    #markup = forms.CharField(widget=MarkItUpWidget(), required=True,
    #    label=_('markup'))
    markup = forms.CharField(widget=forms.Textarea, required=True,
        label=_('markup'))
    #feincms_item_editor_classes = {
    #    'markup': 'markItUp',
    #}

    def __init__(self, *args, **kwargs):
        super(MarkupContentAdminForm, self).__init__(*args, **kwargs)
        self.fields['markup'].widget.attrs.update({'class': 'multiSet'})
        #for field in self.feincms_item_editor_classes.keys():
        #    self.fields[field].widget.attrs.update({'id': '%s' %
        #        self.feincms_item_editor_classes[field]})

    #def save(self, *args, **kwargs):
    #    super(MarkupContentAdminForm, self).save(*args, **kwargs)

    class Meta:
        exclude = ('markup_html',)
