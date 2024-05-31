from typing import Any
from django import forms
from django.contrib.auth import password_validation
from django.core.validators import MinValueValidator
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _
from web.models import Usuario, Inmueble, TipoUsuarioChoices, TipoInmuebleChoices, ComunaChoices, RegionChoices, ContactRequest

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
            'tipo_usuario' : forms.Select(attrs={'class':'form-control'}, choices = TipoUsuarioChoices.choices),
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

class InmuebleForm(forms.ModelForm):
    class Meta:
        model = Inmueble
        fields = ['nombre', 'descripcion', 'm2_construidos', 'm2_totales', 'estacionamientos', 'habitaciones', 'restrooms', 'direccion', 'comuna', 'region', 'tipo_inmueble', 'arriendo' ]
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'La Moneda'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control', 'placeholder':'Descripcion'}),
            'm2_construidos' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'150.0'}),
            'm2_totales' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'150.0'}),
            'estacionamientos' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'habitaciones' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'restrooms' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'2'}),
            'direccion' : forms.TextInput(attrs={'class':'form-control', 'placeholder':'Avenida Siempre Viva 123'}),
            'comuna' : forms.Select(attrs={'class':'form-control'}, choices = ComunaChoices.choices),
            'region' : forms.Select(attrs={'class':'form-control'}, choices = RegionChoices.choices),
            'tipo_inmueble' : forms.Select(attrs={'class':'form-control'}, choices = TipoInmuebleChoices.choices),
            'arriendo' : forms.NumberInput(attrs={'class':'form-control', 'placeholder':'$600.000'}),
        }

class InmuebleFilterForm(forms.Form):
    nombre = forms.CharField(max_length = 50, empty_value = '', required = False, label = 'Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    direccion = forms.CharField(max_length = 50, empty_value = '', required = False, label = 'Direccion', widget=forms.TextInput(attrs={'class': 'form-control'}))
    comuna = forms.ChoiceField(choices = [('', '')] + ComunaChoices.choices, initial = '', required = False, label = 'Comuna', widget=forms.Select(attrs={'class': 'form-control'}))
    region = forms.ChoiceField(choices = [('', '')] + RegionChoices.choices, initial = '', required = False, label = 'Region', widget=forms.Select(attrs={'class': 'form-control'}))
    tipo_inmueble = forms.ChoiceField(choices = [('', '')] + TipoInmuebleChoices.choices , initial = '', required = False, label = 'Tipo de Inmueble', widget=forms.Select(attrs={'class': 'form-control'}))
    m2_construidos_min = forms.FloatField(min_value = 0.0, initial = 0.0, required = False, label = 'Metros² Construidos', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    m2_construidos_max = forms.FloatField(min_value = 0.0, initial = 0.0, required = False, label = 'Metros² Construidos', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    m2_totales_min = forms.FloatField(min_value = 0.0, initial = 0.0, required = False, label = 'Metros² Totales o del terreno', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    m2_totales_max = forms.FloatField(min_value = 0.0, initial = 0.0, required = False, label = 'Metros² Totales o del terreno', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    estacionamientos_min = forms.IntegerField(min_value = 0, initial = 0, required = False, label = 'Cantidad de estacionamientos', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    estacionamientos_max = forms.IntegerField(min_value = 0, initial = 0, required = False, label = 'Cantidad de estacionamientos', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    habitaciones_min = forms.IntegerField(min_value = 0, initial = 0, required = False, label = 'Cantidad de habitaciones', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    habitaciones_max = forms.IntegerField(min_value = 0, initial = 0, required = False, label = 'Cantidad de habitaciones', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    restrooms_min = forms.IntegerField(min_value = 0, initial = 0, required = False, label = 'Cantidad de baños', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    restrooms_max = forms.IntegerField(min_value = 0, initial = 0, required = False, label = 'Cantidad de baños', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    arriendo_min = forms.IntegerField(min_value = 0, initial = 0, required = False, label = 'Precio mensual de arriendo', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    arriendo_max = forms.IntegerField(min_value = 0, initial = 0, required = False, label = 'Precio mensual de arriendo', widget=forms.NumberInput(attrs={'class': 'form-control'}))