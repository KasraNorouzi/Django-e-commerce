from django.contrib.auth import views as auth_views
from .forms import AuthenticationForm


class LoginView(auth_views.LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'accounts/login.html'


class LogoutView(auth_views.LogoutView):
    pass
