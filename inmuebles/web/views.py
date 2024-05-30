from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from web.models import Usuario, Inmueble, ContactRequest
from web.forms import UsuarioModelForm, UsuarioCreationModelForm, UsuarioSetPasswordForm, UsuarioPasswordResetForm, UsuarioPasswordChangeForm, ContactRequestForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView



def index_view(request):
    return render(request, "index.html", {})

def about_view(request):
    return render(request, "about.html", {})

@login_required
def profile_view(request):
    usuario_original = Usuario.objects.get(id = request.user.id)
    if request.method == 'POST':
        # usuario_original = Usuario.objects.filter(email = request.user.email)
        form = UsuarioModelForm(request.POST, instance = usuario_original)
        if form.is_valid():
            # form = form.cleaned_data
            form.save()
            return HttpResponseRedirect('update_success/')
    else:
        form = UsuarioModelForm(instance = usuario_original)

    return render(request, "registration/profile.html", {'form': form})

@login_required
def profile_update_sucess_view(request):
    return render(request, "registration/profile_change_success.html", {})

def signup_view(request):
    if request.method == 'POST':
        form = UsuarioCreationModelForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('signup_success/')
    else:
        form = UsuarioCreationModelForm()

    return render(request, "registration/signup.html", {'form': form})

def signup_success_view(request):
    return render(request, "registration/signup_success.html", {})

class PasswordRecoveryView(PasswordResetView):
    form_class = UsuarioPasswordResetForm
    template_name = 'registration/password_recovery.html'
    success_url = reverse_lazy("password_recovery_done")
    email_template_name = "registration/password_recovery_email.html"
    html_email_template_name = "registration/password_recovery_email.html"
    subject_template_name = "registration/password_recovery_subject.txt"

class PasswordRecoveryDoneView(PasswordResetDoneView):
    template_name = 'registration/password_recovery_done.html'

class PasswordRecoveryConfirmView(PasswordResetConfirmView):
    form_class = UsuarioSetPasswordForm
    template_name = 'registration/password_recovery_confirm.html'
    success_url = reverse_lazy("password_recovery_complete")
    
class PasswordRecoveryCompleteView(PasswordResetCompleteView):
    template_name = 'registration/password_recovery_complete.html'

class UsuarioPasswordChangeView(PasswordChangeView):
    form_class = UsuarioPasswordChangeForm
    success_url = reverse_lazy("password_change_success")
    template_name = 'registration/password_change.html'

class UsuarioPasswordChangeSuccessView(PasswordChangeDoneView):
    template_name = 'registration/password_change_success.html'

def contact_view(request):
    if request.method == 'POST':
        form = ContactRequestForm(request.POST)
        if form.is_valid():
            contact_request = ContactRequest.objects.create(**form.cleaned_data)
            send_mail(
                subject = "Se ha realizado una nueva solicitud de contacto - Inmuebles Kristen",
                message = f"La persona {contact_request.customer_name}, ha enviado el siguiente mensaje:\n{contact_request.message}\nPor favor responder a la brevedadad al siguiente correo: {contact_request.customer_email}",
                from_email = settings.DEFAULT_FROM_EMAIL,
                recipient_list= [settings.DEFAULT_CONTACT_NOTICE_EMAIL]
            )
            return HttpResponseRedirect('success/')
    else:
        form = ContactRequestForm()
    
    return render(request, "contact.html", {'form': form})

def contact_success_view(request):
    return render(request, "contact_success.html", {})