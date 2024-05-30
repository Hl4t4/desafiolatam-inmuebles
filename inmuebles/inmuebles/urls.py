"""
URL configuration for inmuebles project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView
from django.urls import include, path
from web.views import index_view, about_view, contact_view, contact_success_view, profile_view, profile_update_sucess_view, signup_view, signup_success_view, PasswordRecoveryView, PasswordRecoveryDoneView, PasswordRecoveryConfirmView, PasswordRecoveryCompleteView, UsuarioPasswordChangeView, UsuarioPasswordChangeSuccessView
from web.forms import AuthenticationFormWithWidgets


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view),
    path('about/', about_view, name = "about"),
    path('contact/', contact_view, name = "contact"),
    path('contact/success/', contact_success_view, name = "contact_success"),
    path('login/', LoginView.as_view(authentication_form = AuthenticationFormWithWidgets), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('profile/', profile_view),
    path('profile/update_success/', profile_update_sucess_view),
    path('signup/', signup_view, name = 'signup'),
    path('signup/signup_success/', signup_success_view),
    path("password_change/", UsuarioPasswordChangeView.as_view(), name="password_change"),
    path("password_change/success/", UsuarioPasswordChangeSuccessView.as_view(), name="password_change_success"),
    path('password_recovery/', PasswordRecoveryView.as_view(), name = 'password_recovery'),
    path('password_recovery/done/', PasswordRecoveryDoneView.as_view(), name = 'password_recovery_done'),
    path('password_recovery/<uidb64>/<token>/', PasswordRecoveryConfirmView.as_view(), name = 'password_recovery_confirm'),
    path('password_recovery/complete/', PasswordRecoveryCompleteView.as_view(), name = 'password_recovery_complete'),
]
