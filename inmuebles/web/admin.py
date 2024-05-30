from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from web.models import Usuario, Inmueble, Region, Comuna, TipoInmueble, TipoUsuario, SolicitudArriendo

# Register your models here.

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Usuario
        fields = '__all__' 

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = '__all__' 

class UsuarioAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'tipo_usuario', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nombres', 'apellidos', 'rut')
    readonly_fields = ('date_joined',)
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal')}),
        ('Permissions', {'fields': ('tipo_usuario', 'is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'tipo_usuario', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )
    

# admin.site.register(Usuario)
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Inmueble)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(TipoInmueble)
admin.site.register(TipoUsuario)
admin.site.register(SolicitudArriendo)
