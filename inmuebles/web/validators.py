from typing import Any
from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator

class TipoUsuarioValidator (BaseValidator):
    tipos_de_usuario = ['arrendatario', 'arrendador']
    code = 'tipo_usuario_invalido'
    message = f'Valor invalido. Solo {", ".join(tipos_de_usuario)} son validos'

    def compare (self, tipo_de_usuario, tipos_de_usuario) -> bool:
        print (tipo_de_usuario)
        print(tipos_de_usuario)
        return tipo_de_usuario not in tipos_de_usuario
    
    def clean (self, x):
        return x
    
    def __init__(self, foreing_key_field:str, related_field:str, tipos_de_usuario:list = None, message:str = None, code:str = None):
        self.foreing_key_field = foreing_key_field
        self.related_field = related_field
        if tipos_de_usuario is not None:
            self.tipos_de_usuario = tipos_de_usuario
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        super().__init__(limit_value = self.tipos_de_usuario, message = message)

    def __call__ (self, instance):
        related_instance = getattr(instance, self.foreing_key_field)
        if related_instance is not None:
            # raise ValidationError(f'{self.foreing_key_field} no puede ser Nulo.', code = 'null_foreing_key')
        
            print(self.related_field)
            print(related_instance.__dict__)
            value = getattr(related_instance, self.related_field)
            params = {'field': self.related_field,'value': value, 'tipos_de_usuario': ', '.join(self.tipos_de_usuario)}
            if self.compare(value, self.limit_value):
                raise ValidationError (self.message, code = self.code, params = params)
    