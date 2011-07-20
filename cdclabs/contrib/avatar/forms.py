# -*- coding: utf-8 -*-
from django import forms
from contrib.avatar.models import Avatar


class AvatarForm(forms.ModelForm):
    """
    Avatar Input Form
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        instance = None
        try:
            instance = self.user.avatar
        except Exception, e:
            pass
        super(AvatarForm, self).__init__(instance=instance, *args, **kwargs)

    class Meta:
        model = Avatar
        fields = ('avatar',)

    def save(self):
        avatar = super(AvatarForm, self).save(commit=False)
        avatar.user = self.user
        avatar.save()
