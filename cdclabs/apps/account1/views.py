# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, TemplateView
from .generic import MultipleFormMixin, MultipleFormView
from .utils import redirect_to_security_check


class LoginRequiredMixin(object):
    """
    Require user login for all http methods which is similar to decorator
    @login_required to function views.
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class SignupMultipleFormMixin(MultipleFormMixin):
    """
    Sign up form
    """
    form_class = auth.forms.UserCreationForm
    context_form_name = 'signup_form'
    success_url_name = 'account_dashboard'
    submit_url_name = 'account_signup'

    # good example of this flow in django-registration's
    # registration.backends.simple.SimpleBackend.register
    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = auth.authenticate(username=username, password=password)
        auth.login(self.request, user)
        return super(SignupMultipleFormMixin, self).form_valid(form)


class LoginMultipleFormMixin(MultipleFormMixin):
    form_class = auth.forms.AuthenticationForm
    context_form_name = 'login_form'
    success_url_name = 'account_dashboard'
    submit_url_name = 'account_login'

    # see the form_valid flow in django.contrib.auth.views.login
    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return super(LoginMultipleFormMixin, self).form_valid(form)


class SignupLoginView(MultipleFormView):
    multiple_form_mixin_classes = (SignupMultipleFormMixin,
        LoginMultipleFormMixin)
    template_name = 'account/signup_login.html'


class SignupIframeMultipleFormMixin(SignupMultipleFormMixin):
    submit_url_name = 'account_signup_iframe'
    success_url_name = 'account_signup_login_success_iframe'


class LoginIframeMultipleFormMixin(LoginMultipleFormMixin):
    submit_url_name = 'account_login_iframe'
    success_url_name = 'account_signup_login_success_iframe'


class SignupLoginIframeView(MultipleFormView):
    multiple_form_mixin_classes = (SignupIframeMultipleFormMixin,
        LoginIframeMultipleFormMixin)
    template_name = 'signup_login/iframes/signup_login.html'


class SignupLoginSuccessIframeView(TemplateView):
    template_name = 'signup_login/iframes/success.html'


class LogoutView(LoginRequiredMixin, RedirectView):
    """
    Logout view inherit from LoginRequriedMixin and RedirectView
    """
    permanent = False

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        redirect_to = self.request.GET.get(auth.REDIRECT_FIELD_NAME)
        if not redirect_to or not redirect_to_security_check(redirect_to, self.request):
            redirect_to = settings.LOGOUT_REDIRECT_URL
        return redirect_to
