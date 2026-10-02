from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib import messages

from .forms import LoginForm, SignupForm


class LoginView(auth_views.LoginView):
    authentication_form = LoginForm
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class SignupView(CreateView):
    form_class = SignupForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('account')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, 'Аккаунт создан. Вы вошли в систему.')
        return response


class LogoutView(auth_views.LogoutView):
    http_method_names = ['post']


class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/account.html'