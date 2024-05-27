from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
import re

class RutValidator (BaseValidator):
    code = 'rut_invalido'
    message = f'Valor invalido. Solo un RUT valido segun reglas del estado puede ser usado.'

    @staticmethod
    def regex_rut (rut:str) -> bool:
        rut_re = "^([1-9][\d]{6}[\dk])|([1-9][\d]{7}[\dkK])$"
        pattern_rut = re.compile(rut_re)
        # rut_wrong_re = "^(1{7,8}[\dkK])|(2{7,8}[\dkK])|(3{7,8}[\dkK])|(4{7,8}[\dkK])|(5{7,8}[\dkK])|(6{7,8}[\dkK])|(7{7,8}[\dkK])|(8{7,8}[\dkK])|(9{7,8}[\dkK])|(0{7,8}[\dkK])$"
        wrong_rut_re = "^(\d)\1{6,7}[\dkK]$"
        pattern_wrong_rut = re.compile(wrong_rut_re)
        if pattern_rut.match(rut) is None: # En verdad podria levantar error
            # print(rut_re)
            # print(re.search(rut, rut_re))
            # print('rut_re in regex_rut')
            return False
        elif pattern_wrong_rut.match(rut) is None:
            return True
        else:
            # print('rut_wrong_re in regex_rut')
            return False
        
    @staticmethod
    def modulo11(rut:str) -> bool:
        length_rut = len(rut)
        six_counter = 0
        sum = 0
        for index in reversed(range(length_rut-1)):
            number = int(rut[index])
            sum = sum + number * (six_counter + 2)
            six_counter = (six_counter + 1) % 6
        control = sum % 11
        if control == 0:
            control == '0'
        elif control == 1:
            control = 'k'
        else:
            control = str(11-control)
        if control == rut[-1]:
            return True 
        else:
            return False # Podria levantar error
        
    def clean (self, x):
        return x
    
    def __init__(self, rut_field:str, message:str = None, code:str = None):
        self.rut_field = rut_field
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        super().__init__(limit_value = None, message = message)
    
    def __call__ (self, instance):
        if hasattr(instance, self.rut_field):
            rut = getattr(instance, self.rut_field)
        else:
            raise ValidationError(f'{self.rut_field} no puede ser Nulo.', code = 'null_rut')
        if rut is not None:
            params = {'field': self.rut_field,'value': rut}
            # print(rut)
            if self.regex_rut(rut):
                if not self.modulo11(rut):
                    print('modulo11 in __call__')
                    raise ValidationError (self.message, code = self.code, params = params)
            else:
                print('regex rut in __call__')
                raise ValidationError (self.message, code = self.code, params = params)

class TipoUsuarioValidator (BaseValidator):
    tipos_de_usuario = ['arrendatario', 'arrendador']
    code = 'tipo_usuario_invalido'
    message = f'Valor invalido. Solo {", ".join(tipos_de_usuario)} son validos'

    def compare (self, tipo_de_usuario, tipos_de_usuario) -> bool:
        return tipo_de_usuario not in tipos_de_usuario
    
    def clean (self, x):
        return x
    
    def __init__(self, foreing_key_field:str, related_field:list[str], tipos_de_usuario:list = None, message:str = None, code:str = None):
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
        if hasattr(instance, self.foreing_key_field):
            related_instance = getattr(instance, self.foreing_key_field)
        else:
            raise ValidationError(f'{self.foreing_key_field} no puede ser Nulo.', code = 'null_foreing_key')
        if related_instance is not None:
            value = related_instance
            last_related_field = None
            for related_field in self.related_field:
                value = getattr(value, related_field)
                if value is None:
                    raise ValidationError(f'{self.foreing_key_field} no puede ser Nulo.', code = 'null_foreing_key')
                last_related_field = related_field
            params = {'field': last_related_field,'value': value, 'tipos_de_usuario': ', '.join(self.tipos_de_usuario)}
            if self.compare(value, self.limit_value):
                raise ValidationError (self.message, code = self.code, params = params)