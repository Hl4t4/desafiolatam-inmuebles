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
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from web.views import index_view, about_view, contact_view, renter_view, post_rent_view, post_rent_success_view, rentee_view, contact_success_view, profile_view, profile_update_sucess_view, signup_view, signup_success_view, signup_activation_view, signup_activation_success_view, PasswordRecoveryView, PasswordRecoveryDoneView, PasswordRecoveryConfirmView, PasswordRecoveryCompleteView, UsuarioPasswordChangeView, UsuarioPasswordChangeSuccessView
from web.forms import AuthenticationFormWithWidgets


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name = "index"),
    path('about/', about_view, name = "about"),
    path('contact/', contact_view, name = "contact"),
    path('contact/success/', contact_success_view, name = "contact_success"),
    path('login/', LoginView.as_view(authentication_form = AuthenticationFormWithWidgets), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('profile/', profile_view, name = 'profile'),
    path('profile/success/', profile_update_sucess_view, name = "profile_success"),
    path('signup/', signup_view, name = 'signup'),
    path('signup/success/', signup_success_view, name = 'signup_success'),
    path('signup/activation/<uidb64>/<token>/', signup_activation_view, name='signup_activation'),
    path('signup/activation/success/', signup_activation_success_view, name='signup_activation_success'),
    path("password_change/", UsuarioPasswordChangeView.as_view(), name="password_change"),
    path("password_change/success/", UsuarioPasswordChangeSuccessView.as_view(), name="password_change_success"),
    path('password_recovery/', PasswordRecoveryView.as_view(), name = 'password_recovery'),
    path('password_recovery/done/', PasswordRecoveryDoneView.as_view(), name = 'password_recovery_done'),
    path('password_recovery/<uidb64>/<token>/', PasswordRecoveryConfirmView.as_view(), name = 'password_recovery_confirm'),
    path('password_recovery/complete/', PasswordRecoveryCompleteView.as_view(), name = 'password_recovery_complete'),
    path('renter/<str:user>/', renter_view, name = 'renter'),
    path('renter/<str:user>/post_rent/', post_rent_view, name = 'post_rent'),
    path('renter/<str:user>/post_rent/success/', post_rent_success_view, name = 'post_rent_success'),
    path('rentee/<str:user>/', rentee_view, name = 'rentee'),
]
