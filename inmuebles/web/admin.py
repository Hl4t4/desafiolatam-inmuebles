from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from web.models import Usuario, Inmueble

# Register your models here.

class UsuarioAdmin(UserAdmin):
    fieldsets = (
        (None, {
            "fields": (
                
            ),
        }),
    )
    add_fieldsets = (
        (None, {
            "fields": (
                
            ),
        }),
    )
    

admin.site.register(Usuario)
# admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Inmueble)
