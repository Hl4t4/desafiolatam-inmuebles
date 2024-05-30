from django.core.exceptions import ValidationError
from django.core.validators import BaseValidator
import re

class RechazadaVsAceptadaValidator (BaseValidator):
    code = 'estado_invalido'
    message = f'Una solicitud no puede estar rechazada y aceptada al mismo tiempo.'

    def compare (self, aceptada:bool, rechazada:bool) -> bool:
        return aceptada and rechazada
    
    def clean (self, x):
        return x
    
    def __init__(self, aceptada_field:str, rechazada_field:str, message:str = None, code:str = None):
        self.aceptada_field = aceptada_field
        self.rechazada_field = rechazada_field
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        super().__init__(limit_value = None, message = message)

    def __call__ (self, instance):
        if hasattr(instance, self.aceptada_field):
            aceptada = getattr(instance, self.aceptada_field)
        else:
            raise ValidationError(f'{self.aceptada_field} no puede ser Nulo.', code = 'null_aceptada')
        
        if hasattr(instance, self.rechazada_field):
            rechazada = getattr(instance, self.rechazada_field)
        else:
            raise ValidationError(f'{self.rechazada_field} no puede ser Nulo.', code = 'null_rechazada')
        
        if aceptada is not None and rechazada is not None:
            value = aceptada
            self.limit_value = rechazada
            params = {'field': self.aceptada_field,'value': value, self.rechazada_field: rechazada}
            if self.compare(value, self.limit_value):
                raise ValidationError (self.message, code = self.code, params = params)
        else:
             raise ValidationError(f'Ni {self.aceptada} ni {self.rechazada} pueden ser Nulos.', code = 'null_m2')

class TerrenoVsConstruidoValidator (BaseValidator):
    code = 'terreno_invalido'
    message = f'El valor del terreno construido no es valido.'

    def compare (self, m2_construidos:float, m2_totales:float) -> bool:
        return m2_construidos > m2_totales
    
    def clean (self, x):
        return x
    
    def __init__(self, contruido_field:str, total_field:str, message:str = None, code:str = None):
        self.contruido_field = contruido_field
        self.total_field = total_field
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        super().__init__(limit_value = None, message = message)

    def __call__ (self, instance):
        if hasattr(instance, self.contruido_field):
            m2_contruidos = getattr(instance, self.contruido_field)
        else:
            raise ValidationError(f'{self.contruido_field} no puede ser Nulo.', code = 'null_m2_construidos')
        if hasattr(instance, self.total_field):
            m2_totales = getattr(instance, self.total_field)
        else:
            raise ValidationError(f'{self.total_field} no puede ser Nulo.', code = 'null_m2_totales')
        
        if m2_contruidos is not None and m2_totales is not None:
            value = m2_contruidos
            self.limit_value = m2_totales
            params = {'field': self.contruido_field,'value': value, self.total_field: m2_totales}
            if self.compare(value, self.limit_value):
                raise ValidationError (self.message, code = self.code, params = params)
        else:
             raise ValidationError(f'Ni {self.total_field} ni {self.contruido_field} pueden ser Nulos.', code = 'null_m2')

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
            control = '0'

        elif control == 1:
            control = 'k'

        else:
            control = str(11-control)

        if control == rut[-1]:
            return True 
        
        else:
            return False
        
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
            rut = rut.replace('.', '').replace('-', '')
            if self.regex_rut(rut):
                # print(rut)
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