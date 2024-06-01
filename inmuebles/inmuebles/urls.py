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
from web.views import index_view, about_view, contact_view, renter_view, renter_applications_view, renter_update_application_view, renter_accepted_applications_view, renter_rejected_applications_view, renter_add_rent_view, renter_add_rent_success_view, renter_update_rent_view, renter_delete_rent_view,  rentee_view, rentee_accepted_applications_view, rentee_rejected_applications_view, rentee_rents_view, rentee_add_application_view, contact_success_view, profile_view, profile_update_sucess_view, signup_view, signup_success_view, signup_activation_view, signup_activation_success_view, not_authorized_view, PasswordRecoveryView, PasswordRecoveryDoneView, PasswordRecoveryConfirmView, PasswordRecoveryCompleteView, UsuarioPasswordChangeView, UsuarioPasswordChangeSuccessView
from web.forms import AuthenticationFormWithWidgets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index_view, name = "index"),
    path('about/', about_view, name = "about"),
    path('contact/', contact_view, name = "contact"),
    path('contact/success/', contact_success_view, name = "contact_success"),
    path('login/', LoginView.as_view(authentication_form = AuthenticationFormWithWidgets), name='login'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('not_authorized/', not_authorized_view, name='not_authorized'),
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
    path('renter/<str:user>/add_rent/', renter_add_rent_view, name = 'renter_add_rent'),
    path('renter/<str:user>/add_rent/success/', renter_add_rent_success_view, name = 'renter_add_rent_success'),
    path('renter/<str:user>/update/<str:inmueble>/', renter_update_rent_view, name = 'renter_update_rent'),
    path('renter/<str:user>/delete/<str:inmueble>/', renter_delete_rent_view, name = 'renter_delete_rent'),
    path('renter/<str:user>/applications/', renter_applications_view, name = 'renter_applications'),
    path('renter/<str:user>/applications/<str:application>/', renter_update_application_view, name = 'renter_update_application'),
    path('renter/<str:user>/accepted_applications/', renter_accepted_applications_view, name = 'renter_accepted_applications'),
    path('renter/<str:user>/rejected_applications/', renter_rejected_applications_view, name = 'renter_rejected_applications'),
    path('rentee/<str:user>/', rentee_view, name = 'rentee'),
    path('rentee/<str:user>/accepted_applications/', rentee_accepted_applications_view, name = 'rentee_accepted_applications'),
    path('rentee/<str:user>/rejected_applications/', rentee_rejected_applications_view, name = 'rentee_rejected_applications'),
    path('rentee/<str:user>/rents/', rentee_rents_view, name = 'rentee_rents'),
    path('rentee/<str:user>/rents/<str:inmueble>/', rentee_add_application_view, name = 'rentee_add_application'),
]
