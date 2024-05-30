from typing import Any
from django import forms
from django.contrib.auth import password_validation
# from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from web.models import Usuario, Inmueble, TipoUsuarioChoices, ContactRequest

class AuthenticationFormWithWidgets(AuthenticationForm):
    username = forms.EmailField(
        label=_("Correo de usuario"), 
        widget=forms.TextInput(attrs={"autofocus": True, 'class':'form-control', 'placeholder':'Correo de usuario'}))
    password = forms.CharField(
        label=_("Contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class':'form-control', 'placeholder':'*****************'}),
    )

class UsuarioModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        # fields = ['email', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'tipo_usuario', 'date_joined']
        fields = ['email', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'tipo_usuario']
        widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'correo@dominio.cl'}),
            'nombres' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombres'}),
            'apellidos' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombres'}),
            'rut' : forms.TextInput(attrs={'class':'form-control rut', 'placeholder':'XX.XXX.XXX-X'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Avenida Siempre Viva 123'}),
            'telefono_personal' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'XXXXXXXXX'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Avenida Siempre Viva 123'}),
            'tipo_usuario' : forms.Select(choices = TipoUsuarioChoices.choices),
            # 'date_joined' : forms.DateInput(attrs={'readonly': 'readonly', 'class':'form-control'})
        }
    
    # def __init__(self, *args, **kwargs):
    #     super(UsuarioModelForm, self).__init__(*args, **kwargs)
    #     self.fields['date_joined'].disabled = True
class UsuarioCreationModelForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['email', 'password1', 'password2', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'tipo_usuario']
        widgets = {
            'email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'correo@dominio.cl'}),
            'password1' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'*****************'}),
            'password2' : forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'*****************'}),
            'nombres' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombres'}),
            'apellidos' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombres'}),
            'rut' : forms.TextInput(attrs={'class':'form-control rut', 'placeholder':'XX.XXX.XXX-X'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Avenida Siempre Viva 123'}),
            'telefono_personal' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'XXXXXXXXX'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Avenida Siempre Viva 123'}),
            'tipo_usuario' : forms.Select(choices = TipoUsuarioChoices.choices),
            # 'date_joined' : forms.DateInput(attrs={'readonly': 'readonly', 'class':'form-control'})
        }
        
class UsuarioPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", 'class':'form-control', 'placeholder':'correo@dominio.cl'}),
    )
    def get_users(self, email:str) -> Usuario:
        usuarios = Usuario.objects.filter(email__iexact = email, is_active = True)
        return (usuario for usuario in usuarios if usuario.has_usable_password())

class UsuarioSetPasswordForm(SetPasswordForm):
    error_messages = {
        "password_mismatch": _("Las dos contraseñas no coinciden."),
    }
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control', 'placeholder':'*****************'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirmación de Nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control', 'placeholder':'*****************'}),
    )
    def __init__(self, user: Usuario | None, *args: Any, **kwargs: Any) -> None:
        super().__init__(user, *args, **kwargs)
        self.user = user

class UsuarioPasswordChangeForm(PasswordChangeForm):
    error_messages = {
        **SetPasswordForm.error_messages, "password_incorrect": _("Su contraseña antigua es incorrecta. Introduzcala de nuevo por favor."),
    }
    old_password = forms.CharField(
        label=_("Contraseña Antigua"),
        strip=False,
        widget=forms.PasswordInput(
            # attrs={"autocomplete": "current-password", "autofocus": True}
            attrs={"autofocus": True, 'class':'form-control', 'placeholder':'*****************'}
        ),
    )
    new_password1 = forms.CharField(
        label=_("Nueva contraseña"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control', 'placeholder':'*****************'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("Confirmación de Nueva contraseña"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class':'form-control', 'placeholder':'*****************'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_password_form = UsuarioSetPasswordForm(user=self.user)

class ContactRequestForm(forms.ModelForm):
    class Meta:
        model = ContactRequest
        fields = ['customer_email', 'customer_name', 'message']
        widgets = {
            'customer_email' : forms.EmailInput(attrs={'class':'form-control', 'placeholder':'correo@dominio.cl'}),
            'customer_name' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'message' : forms.Textarea(attrs={'class':'form-control'}),
        }