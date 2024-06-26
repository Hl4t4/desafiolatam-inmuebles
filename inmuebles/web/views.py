from django.core.mail import send_mail
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from web.models import Usuario, Inmueble, Comuna, Region, ContactRequest, SolicitudArriendo, TipoInmueble, TipoUsuario
from web.forms import UsuarioModelForm, UsuarioCreationModelForm, UsuarioSetPasswordForm, UsuarioPasswordResetForm, UsuarioPasswordChangeForm, ContactRequestForm, InmuebleForm, InmuebleFilterForm, SolicitudArriendoForm, SolicitudArriendoModifiableForm
from web.decorators import tipo_usuario_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def index_view(request):
    inmuebles = Inmueble.objects.filter(arrendador = None) # Exclude para lo opuesto
    context = {'inmuebles': inmuebles}
    return render(request, "index.html", context)

def not_authorized_view(request):
    return render(request, "not_authorized.html", {})

def about_view(request):
    return render(request, "about.html", {})

@login_required
def profile_view(request):
    usuario_original = Usuario.objects.get(id = request.user.id)
    if request.method == 'POST':
        form = UsuarioModelForm(request.POST, instance = usuario_original)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('success/')
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
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activa Tu Cuenta'
            message = render_to_string('registration/signup_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'protocol': 'https',
                'site_name': current_site.name,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message= message)
            return HttpResponseRedirect('success/')
    else:
        form = UsuarioCreationModelForm()

    return render(request, "registration/signup.html", {'form': form})

def signup_success_view(request):
    return render(request, "registration/signup_success.html", {})

def signup_activation_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = Usuario.objects.get(pk = uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponseRedirect('/signup/activation/success/') # Puede estar malo
    else:
        return render(request, 'registration/signup_activation_invalid.html')
    
def signup_activation_success_view(request):
    return render(request, "registration/signup_activation_success.html", {})

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
                recipient_list= [contact_request.customer_email]
            )
            return HttpResponseRedirect('success/')
    else:
        form = ContactRequestForm()
    
    return render(request, "contact.html", {'form': form})

def contact_success_view(request):
    return render(request, "contact_success.html", {})

@login_required
@tipo_usuario_required('arrendatario')
def renter_view(request, user:Usuario):
    if request.method == 'POST':
        form = InmuebleFilterForm(request.POST)
        if form.is_valid():
            real_filters = {key:value for key,value in form.cleaned_data.items() if value != "" and value != 0} # Eliminar filtros no usados
            inmuebles = Inmueble.objects.filter(arrendatario = request.user)
            model_mapping = {
                'tipo_inmueble': [TipoInmueble , 'nombre_tipo_inmueble'],
                'tipo_usuario': [TipoUsuario, 'nombre_tipo_usuario'], 
                'comuna': [Comuna, 'nombre_comuna'],
                'region': [Region, 'nombre_region']
                }
            # PROBAR CON RAWQUERY
            for key, value in real_filters.items():
                if type(value) == int or type(value) == float:
                    if 'min' in key:
                        filter_params = {f'{key[0:-4]}__gte': value}
                    else:
                        filter_params = {f'{key[0:-4]}__lte': value}
                    inmuebles = inmuebles.filter(**filter_params)
                elif key in model_mapping:
                    model = model_mapping[key]
                    filter_params = {model[1]: value}
                    related_model = model[0].objects.get(**filter_params)
                    filter_params = {key: related_model}
                    inmuebles = inmuebles.filter(**filter_params)
                elif type(value) == str:
                    filter_params = {f'{key}__icontains': value}
                    inmuebles = inmuebles.filter(**filter_params)
                else:
                    filter_params = {key: value}
                    inmuebles = inmuebles.filter(**filter_params)
            context = {"inmuebles" : inmuebles, 
                    "form" : form,}
            return render(request, "renter.html", context)

    else:
        inmuebles = Inmueble.objects.filter(arrendatario = request.user)
        form = InmuebleFilterForm()
        context = {"inmuebles" : inmuebles, 
                   "form" : form,}
        return render(request, "renter.html", context)

@login_required
@tipo_usuario_required('arrendatario')
def renter_add_rent_view(request, user:Usuario):
    if request.method == 'POST':
        form = InmuebleForm(request.POST)
        if form.is_valid():
            inmueble = form.save(commit=False)
            inmueble.arrendatario = request.user
            inmueble.arrendador = None
            inmueble.save()
            return HttpResponseRedirect('success/')
    else:
        user = Usuario.objects.get(id = request.user.id)
        initial_data = {}
        initial_data['arrendatario'] = user
        form = InmuebleForm(initial = initial_data)
    
    return render(request, "renter_add_rent.html", {'form': form})

@login_required
@tipo_usuario_required('arrendatario')
def renter_add_rent_success_view(request, user:Usuario):
    return render(request, "renter_add_rent_success.html", {})

@login_required
@tipo_usuario_required('arrendatario')
def renter_update_rent_view(request, user:Usuario, inmueble:Inmueble):
    inmueble_original = Inmueble.objects.get(id = inmueble)
    if request.method == 'POST':
        form = InmuebleForm(request.POST, instance = inmueble_original)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/renter/' + user + '/')
    else:
        form = InmuebleForm(instance = inmueble_original)
    return render(request, "renter_update_rent.html", {'form': form, 'inmueble': inmueble_original})

@login_required
@tipo_usuario_required('arrendatario')
def renter_delete_rent_view(request, user:Usuario, inmueble:Inmueble):
    to_be_deleted_inmueble = Inmueble.objects.get(id = inmueble)
    usuario = Usuario.objects.get(id = user)
    if request.user.id == int(user) and to_be_deleted_inmueble.arrendatario == usuario:
        to_be_deleted_inmueble.delete()
    return HttpResponseRedirect('/renter/' + user + '/')

@login_required
@tipo_usuario_required('arrendatario')
def renter_applications_view(request, user:Usuario):
    inmuebles = Inmueble.objects.filter(arrendatario = request.user) 
    solicitudes_arriendo =  SolicitudArriendo.objects
    solicitudes_arriendo =  solicitudes_arriendo.filter(inmueble__in = inmuebles)
    context = {'inmuebles': inmuebles,
               'solicitudes_arriendo': solicitudes_arriendo}
    return render(request, "renter_applications.html", context)

@login_required
@tipo_usuario_required('arrendatario')
def renter_update_application_view(request, user:Usuario, application:SolicitudArriendo):
    solicitud_arriendo = SolicitudArriendo.objects.get(id = application)
    arrendador = solicitud_arriendo.arrendador
    inmueble = solicitud_arriendo.inmueble
    if request.method == 'POST':
        form = SolicitudArriendoModifiableForm(request.POST, instance = solicitud_arriendo)
        if form.is_valid():
            form.save()
            if solicitud_arriendo.aceptada:
                inmueble.arrendador = arrendador
                inmueble.save()
            return HttpResponseRedirect('/renter/' + user + '/applications/')
        else:
            context = {'form': form,
                'arrendador': arrendador,
                'inmueble': inmueble,
                'application': application}        
            return render(request, "renter_modify_application.html", context)
    prefill = {'arrendador' : arrendador.id, 'inmueble' : inmueble.id, 'aceptada' : False, 'rechazada' : False}
    form = SolicitudArriendoModifiableForm(pre_filled_value = prefill)
    context = {'form': form,
                'arrendador': arrendador,
                'inmueble': inmueble,
                'application': application}
    return render(request, "renter_modify_application.html", context)

@login_required
@tipo_usuario_required('arrendatario')
def renter_accepted_applications_view(request, user:Usuario):
    inmuebles = Inmueble.objects.filter(arrendatario = request.user) 
    solicitudes_arriendo =  SolicitudArriendo.objects
    solicitudes_arriendo =  solicitudes_arriendo.filter(inmueble__in = inmuebles)
    solicitudes_arriendo =  solicitudes_arriendo.filter(aceptada = True)
    context = {'inmuebles': inmuebles,
               'solicitudes_arriendo': solicitudes_arriendo}
    return render(request, "renter_applications.html", context)

@login_required
@tipo_usuario_required('arrendatario')
def renter_rejected_applications_view(request, user:Usuario):
    inmuebles = Inmueble.objects.filter(arrendatario = request.user) 
    solicitudes_arriendo =  SolicitudArriendo.objects
    solicitudes_arriendo =  solicitudes_arriendo.filter(inmueble__in = inmuebles)
    solicitudes_arriendo =  solicitudes_arriendo.filter(rechazada = True)
    context = {'inmuebles': inmuebles,
               'solicitudes_arriendo': solicitudes_arriendo}
    return render(request, "renter_applications.html", context)

@login_required
@tipo_usuario_required('arrendador')
def rentee_view(request, user:Usuario):
    inmuebles = Inmueble.objects.filter(arrendador = None).exclude(arrendatario = request.user)
    solicitudes_arriendo =  SolicitudArriendo.objects.filter(arrendador = request.user)
    for solicitud_arriendo in solicitudes_arriendo:
        inmuebles = inmuebles.exclude(id = solicitud_arriendo.inmueble.id)
    context = {'inmuebles': inmuebles,
               'solicitudes_arriendo': solicitudes_arriendo}
    return render(request, "rentee.html", context)

@login_required
@tipo_usuario_required('arrendador')
def rentee_accepted_applications_view(request, user:Usuario):
    inmuebles = Inmueble.objects.filter(arrendador = None).exclude(arrendatario = request.user)
    solicitudes_arriendo =  SolicitudArriendo.objects.filter(arrendador = request.user)
    for solicitud_arriendo in solicitudes_arriendo:
        inmuebles = inmuebles.exclude(id = solicitud_arriendo.inmueble.id)
    solicitudes_arriendo =  solicitudes_arriendo.filter(aceptada = True)
    context = {'inmuebles': inmuebles,
               'solicitudes_arriendo': solicitudes_arriendo}
    return render(request, "rentee.html", context)

@login_required
@tipo_usuario_required('arrendador')
def rentee_rejected_applications_view (request, user:Usuario):
    inmuebles = Inmueble.objects.filter(arrendador = None).exclude(arrendatario = request.user)
    solicitudes_arriendo =  SolicitudArriendo.objects.filter(arrendador = request.user)
    for solicitud_arriendo in solicitudes_arriendo:
        inmuebles = inmuebles.exclude(id = solicitud_arriendo.inmueble.id)
    solicitudes_arriendo =  solicitudes_arriendo.filter(rechazada = True)
    context = {'inmuebles': inmuebles,
               'solicitudes_arriendo': solicitudes_arriendo}
    return render(request, "rentee.html", context)


@login_required
@tipo_usuario_required('arrendador')
def rentee_rents_view(request, user:Usuario):
    inmuebles = Inmueble.objects.filter(arrendador = None).exclude(arrendatario = request.user) 
    solicitudes_arriendo =  SolicitudArriendo.objects.filter(arrendador = request.user)
    for solicitud_arriendo in solicitudes_arriendo:
        inmuebles = inmuebles.exclude(id = solicitud_arriendo.inmueble.id)
    if request.method == 'POST':
        form = InmuebleFilterForm(request.POST)
        if form.is_valid():
            real_filters = {key:value for key,value in form.cleaned_data.items() if value != "" and value != 0} # Eliminar filtros no usados
            model_mapping = {
                'tipo_inmueble': [TipoInmueble , 'nombre_tipo_inmueble'],
                'tipo_usuario': [TipoUsuario, 'nombre_tipo_usuario'], 
                'comuna': [Comuna, 'nombre_comuna'],
                'region': [Region, 'nombre_region']
                }
            # PROBAR CON RAWQUERY
            for key, value in real_filters.items():
                if type(value) == int or type(value) == float:
                    if 'min' in key:
                        filter_params = {f'{key[0:-4]}__gte': value}
                    else:
                        filter_params = {f'{key[0:-4]}__lte': value}
                    inmuebles = inmuebles.filter(**filter_params)
                elif key in model_mapping:
                    model = model_mapping[key]
                    filter_params = {model[1]: value}
                    related_model = model[0].objects.get(**filter_params)
                    filter_params = {key: related_model}
                    inmuebles = inmuebles.filter(**filter_params)
                elif type(value) == str:
                    filter_params = {f'{key}__icontains': value}
                    inmuebles = inmuebles.filter(**filter_params)
                else:
                    filter_params = {key: value}
                    inmuebles = inmuebles.filter(**filter_params)
    else:
        form = InmuebleFilterForm()
    context = {"inmuebles" : inmuebles, 
                "form" : form,}
    return render(request, "rentee_rents.html", context)

@login_required
@tipo_usuario_required('arrendador')
def rentee_add_application_view(request, user:Usuario, inmueble:Inmueble):
    inmueble = Inmueble.objects.get(id = inmueble)
    if request.method == 'POST':
        form = SolicitudArriendoForm(request.POST)
        if form.is_valid():
            solicitud_arriendo = SolicitudArriendo.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/rentee/' + user + '/')
    else:
        prefill = {'arrendador' : user, 'inmueble' : inmueble, 'aceptada' : False, 'rechazada' : False}
        form = SolicitudArriendoForm(pre_filled_value = prefill)
        if form.is_valid():
            solicitud_arriendo = SolicitudArriendo.objects.create(**form.cleaned_data)
            return HttpResponseRedirect('/rentee/' + user + '/')
    context = {'inmueble': inmueble,
               'form': form}
    return render(request, "rentee_add_application.html", context)


