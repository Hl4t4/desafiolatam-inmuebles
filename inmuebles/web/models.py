from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MinLengthValidator
from web.validators import TipoUsuarioValidator, RutValidator, TerrenoVsConstruidoValidator, RechazadaVsAceptadaValidator
from datetime import date


# Create your models here.


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Se debe usar un correo electronico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        # print(user)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class Usuario (AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique = True, null = False, blank = False, verbose_name = 'Correo Electronico')
    password = models.CharField(validators = [MinLengthValidator(8)], max_length=128, verbose_name = "Contraseña")
    nombres = models.CharField(max_length = 50, null = False, blank = False, verbose_name = 'Nombres')
    apellidos = models.CharField(max_length = 50, null = False, blank = False, verbose_name = 'Apellidos')
    rut = models.CharField(max_length = 12, null = False, blank = False, verbose_name = 'RUT')
    direccion = models.CharField(max_length = 50, null = False, blank = True, verbose_name = 'Direccion')
    telefono_personal = models.PositiveIntegerField(null = False, blank = True, verbose_name = 'Telefono Personal', validators=[MinValueValidator(0)])
    tipo_usuario = models.ForeignKey(to = "TipoUsuario", on_delete = models.CASCADE, null = True, blank = True)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True, verbose_name = "Esta el usuario activo?")
    date_joined = models.DateTimeField(auto_now_add = True)
    date_modified = models.DateTimeField(auto_now = True)

    
    objects = UsuarioManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS =['nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal']

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    def clean(self):
        validator_rut = RutValidator(rut_field = 'rut')
        validator_rut(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    @staticmethod
    def format_rut(rut:str) -> str:
        body = rut[:-1]
        verifier = rut[-1]
        return f'{body[:-6]}.{body[-6:-3]}.{body[-3:]}-{verifier}'

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'
        # return f'Nombre: {self.nombres} {self.apellidos}\nRUT: {self.format_rut(self.rut)}\nDireccion: {self.direccion}\nTelefono: {self.telefono_personal}\nCorreo Electronico: {self.email}\nTipo de Usuario: {self.tipo_usuario}'

class Inmueble (models.Model):
    nombre = models.CharField(max_length = 50, null = False, blank = False, verbose_name = 'Nombre')
    descripcion = models.TextField(null = False, blank = True, verbose_name = 'Descripcion')
    m2_construidos = models.FloatField(null = False, blank = False, validators=[MinValueValidator(0.0)], verbose_name = 'Metros² Construidos')
    m2_totales = models.FloatField(null = False, blank = False, validators=[MinValueValidator(0.0)], verbose_name = 'Metros² Totales o del terreno')
    estacionamientos = models.PositiveIntegerField(null = False, blank = False, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de estacionamientos')
    habitaciones = models.PositiveIntegerField(null = False, blank = False, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de habitaciones')
    restrooms = models.PositiveIntegerField(null = False, blank = False, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de baños')
    direccion = models.CharField(max_length = 50, null = False, blank = True, verbose_name = 'Direccion')
    comuna = models.ForeignKey(to = "Comuna", on_delete = models.CASCADE, verbose_name = 'Comuna')
    region = models.ForeignKey(to = "Region", on_delete = models.CASCADE, verbose_name = 'Region')
    tipo_inmueble = models.ForeignKey(to = "TipoInmueble", on_delete = models.CASCADE)
    arriendo = models.PositiveIntegerField(null = False, blank = False, validators=[MinValueValidator(0)], verbose_name = 'Precio mensual de arriendo')
    arrendador = models.ForeignKey(Usuario, null=True, blank=True, on_delete = models.CASCADE, related_name = 'inmueble_arrendador')
    arrendatario = models.ForeignKey(Usuario, null = True, blank = False, on_delete = models.CASCADE, related_name = 'inmueble_arrendatario')

    
    def clean(self):
        validator_arrendador = TipoUsuarioValidator(foreing_key_field = 'arrendador', related_field = ['tipo_usuario', 'nombre_tipo_usuario'], tipos_de_usuario = ['arrendador'])
        validator_arrendatario = TipoUsuarioValidator(foreing_key_field = 'arrendatario', related_field = ['tipo_usuario', 'nombre_tipo_usuario'], tipos_de_usuario = ['arrendatario'])
        validator_metros = TerrenoVsConstruidoValidator(contruido_field = 'm2_construidos', total_field = 'm2_totales')
        validator_arrendador(self)
        validator_arrendatario(self)
        validator_metros(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        
    def as_dict(self):
        return {
            "nombre": self.nombre,
            "descripcion": self.descripcion,
            "m2_construidos": self.m2_construidos,
            "m2_totales": self.m2_totales,
            "estacionamientos": self.estacionamientos,
            "habitaciones": self.habitaciones,
            "restrooms": self.restrooms,
            "direccion": self.direccion,
            "comuna": self.comuna.nombre_comuna if self.comuna else None,
            "region": self.region.nombre_region if self.region else None,
            "tipo_inmueble": self.tipo_inmueble.nombre_tipo_inmueble if self.tipo_inmueble else None,
            "arriendo": self.arriendo,
            "arrendador": self.arrendador.nombres + ' ' + self.arrendador.apellidos if self.arrendador else "No hay arrendador", # Assuming arrendador and arrendatario are ForeignKey fields
            "arrendatario": self.arrendatario.nombres + ' ' + self.arrendatario.apellidos if self.arrendatario else None,
        }


    def __str__(self):
        return f'Nombre: {self.nombre}\nDescripcion: {self.descripcion}\nMetros² Construidos: {self.m2_construidos}[m²]\nMetros Totales o del Terreno: {self.m2_totales}[m²]\nCantidad de estacionamientos: {self.estacionamientos}\nCantidad de habitaciones: {self.habitaciones}\nCantidad de baños: {self.restrooms}\nDireccion: {self.direccion}, {self.comuna}, {self.region}\nTipo de Inmueble: {self.tipo_inmueble}\nPrecio mensual de arriendo: ${self.arriendo}'

class SolicitudArriendo (models.Model):
    arrendador = models.OneToOneField(Usuario, on_delete=models.CASCADE, verbose_name = "Arrendador")
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE, verbose_name = "Inmueble")
    aceptada = models.BooleanField(default = False, null = False, verbose_name = "Ha sido aceptada la solicitud?")
    rechazada = models.BooleanField(default = False, null = False, verbose_name = "Ha sido rechazada la solicitud?") # Se necesita validador que no pueden estar los dos positivos al mismo tiempo

    def clean(self):
        validator_arrendador = TipoUsuarioValidator(foreing_key_field = 'arrendador', related_field = 'tipo_usuario', tipos_de_usuario = ['arrendador'])
        validator_aceptadas = RechazadaVsAceptadaValidator(aceptada_field = 'aceptada', rechazada_field = 'rechazada')
        validator_arrendador(self)
        validator_aceptadas(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'El arrendador\n{self.arrendador}\nDesea arrendar el inmueble\n{self.inmueble}\nLa solicitud se encuentra aceptada: {self.aceptada}'

class ComunaChoices (models.TextChoices):
    ARICA = "Arica", "Arica"
    CAMARONES = "Camarones", "Camarones"
    PUTRE = "Putre", "Putre"
    GENERAL_LAGOS = "General Lagos", "General Lagos"
    IQUIQUE = "Iquique", "Iquique"
    ALTO_HOSPICIO = "Alto Hospicio", "Alto Hospicio"
    POZO_ALMONTE = "Pozo Almonte", "Pozo Almonte"
    CAMINA = "Camiña", "Camiña"
    COLCHANE = "Colchane", "Colchane"
    HUARA = "Huara", "Huara"
    PICA = "Pica", "Pica"
    ANTOFAGASTA = "Antofagasta", "Antofagasta"
    MEJILLONES = "Mejillones", "Mejillones"
    SIERRA_GORDA = "Sierra Gorda", "Sierra Gorda"
    TALTAL = "Taltal", "Taltal"
    CALAMA = "Calama", "Calama"
    OLLAGUE = "Ollagüe", "Ollagüe"
    SAN_PEDRO_DE_ATACAMA = "San Pedro de Atacama", "San Pedro de Atacama"
    TOCOPILLA = "Tocopilla", "Tocopilla"
    MARIA_ELENA = "María Elena", "María Elena"
    COPIAPO = "Copiapó", "Copiapó"
    CALDERA = "Caldera", "Caldera"
    TIERRA_AMARILLA = "Tierra Amarilla", "Tierra Amarilla"
    CHANARAL = "Chañaral", "Chañaral"
    DIEGO_DE_ALMAGRO = "Diego de Almagro", "Diego de Almagro"
    VALLENAR = "Vallenar", "Vallenar"
    ALTO_DEL_CARMEN = "Alto del Carmen", "Alto del Carmen"
    FREIRINA = "Freirina", "Freirina"
    HUASCO = "Huasco", "Huasco"
    LA_SERENA = "La Serena", "La Serena"
    COQUIMBO = "Coquimbo", "Coquimbo"
    ANDACOLLO = "Andacollo", "Andacollo"
    LA_HIGUERA = "La Higuera", "La Higuera"
    PAIGUANO = "Paiguano", "Paiguano"
    VICUNA = "Vicuña", "Vicuña"
    ILLAPEL = "Illapel", "Illapel"
    CANELA = "Canela", "Canela"
    LOS_VILOS = "Los Vilos", "Los Vilos"
    SALAMANCA = "Salamanca", "Salamanca"
    OVALLE = "Ovalle", "Ovalle"
    COMBARBALA = "Combarbalá", "Combarbalá"
    MONTE_PATRIA = "Monte Patria", "Monte Patria"
    PUNITAQUI = "Punitaqui", "Punitaqui"
    RIO_HURTADO = "Río Hurtado", "Río Hurtado"
    VALPARAISO = "Valparaíso", "Valparaíso"
    CASABLANCA = "Casablanca", "Casablanca"
    CONCON = "Concón", "Concón"
    JUAN_FERNANDEZ = "Juan Fernández", "Juan Fernández"
    PUCHUNCAVI = "Puchuncaví", "Puchuncaví"
    QUINTERO = "Quintero", "Quintero"
    VINA_DEL_MAR = "Viña del Mar", "Viña del Mar"
    ISLA_DE_PASCUA = "Isla de Pascua", "Isla de Pascua"
    LOS_ANDES = "Los Andes", "Los Andes"
    CALLE_LARGA = "Calle Larga", "Calle Larga"
    RINCONADA = "Rinconada", "Rinconada"
    SAN_ESTEBAN = "San Esteban", "San Esteban"
    LA_LIGUA = "La Ligua", "La Ligua"
    CABILDO = "Cabildo", "Cabildo"
    PAPUDO = "Papudo", "Papudo"
    PETORCA = "Petorca", "Petorca"
    ZAPALLAR = "Zapallar", "Zapallar"
    QUILLOTA = "Quillota", "Quillota"
    CALERA = "Calera", "Calera"
    HIJUELAS = "Hijuelas", "Hijuelas"
    LA_CRUZ = "La Cruz", "La Cruz"
    NOGALES = "Nogales", "Nogales"
    SAN_ANTONIO = "San Antonio", "San Antonio"
    ALGARROBO = "Algarrobo", "Algarrobo"
    CARTAGENA = "Cartagena", "Cartagena"
    EL_QUISCO = "El Quisco", "El Quisco"
    EL_TABO = "El Tabo", "El Tabo"
    SANTO_DOMINGO = "Santo Domingo", "Santo Domingo"
    SAN_FELIPE = "San Felipe", "San Felipe"
    CATEMU = "Catemu", "Catemu"
    LLAILLAY = "Llaillay", "Llaillay"
    PANQUEHUE = "Panquehue", "Panquehue"
    PUTAENDO = "Putaendo", "Putaendo"
    SANTA_MARIA = "Santa María", "Santa María"
    QUILPUE = "Quilpué", "Quilpué"
    LIMACHE = "Limache", "Limache"
    OLMUE = "Olmué", "Olmué"
    VILLA_ALEMANA = "Villa Alemana", "Villa Alemana"
    RANCAGUA = "Rancagua", "Rancagua"
    CODEGUA = "Codegua", "Codegua"
    COINCO = "Coinco", "Coinco"
    COLTAUCO = "Coltauco", "Coltauco"
    DONIHUE = "Doñihue", "Doñihue"
    GRANEROS = "Graneros", "Graneros"
    LAS_CABRAS = "Las Cabras", "Las Cabras"
    MACHALI = "Machalí", "Machalí"
    MALLOA = "Malloa", "Malloa"
    MOSTAZAL = "Mostazal", "Mostazal"
    OLIVAR = "Olivar", "Olivar"
    PEUMO = "Peumo", "Peumo"
    PICHIDEGUA = "Pichidegua", "Pichidegua"
    QUINTA_DE_TILCOCO = "Quinta de Tilcoco", "Quinta de Tilcoco"
    RENGO = "Rengo", "Rengo"
    REQUINOA = "Requínoa", "Requínoa"
    SAN_VICENTE = "San Vicente", "San Vicente"
    PICHILEMU = "Pichilemu", "Pichilemu"
    LA_ESTRELLA = "La Estrella", "La Estrella"
    LITUECHE = "Litueche", "Litueche"
    MARCHIHUE = "Marchihue", "Marchihue"
    NAVIDAD = "Navidad", "Navidad"
    PAREDONES = "Paredones", "Paredones"
    SAN_FERNANDO = "San Fernando", "San Fernando"
    CHEPICA = "Chépica", "Chépica"
    CHIMBARONGO = "Chimbarongo", "Chimbarongo"
    LOLOL = "Lolol", "Lolol"
    NANCAGUA = "Nancagua", "Nancagua"
    PALMILLA = "Palmilla", "Palmilla"
    PERALILLO = "Peralillo", "Peralillo"
    PLACILLA = "Placilla", "Placilla"
    PUMANQUE = "Pumanque", "Pumanque"
    SANTA_CRUZ = "Santa Cruz", "Santa Cruz"
    TALCA = "Talca", "Talca"
    CONSTITUCION = "Constitución", "Constitución"
    CUREPTO = "Curepto", "Curepto"
    EMPEDRADO = "Empedrado", "Empedrado"
    MAULE = "Maule", "Maule"
    PELARCO = "Pelarco", "Pelarco"
    PENCAHUE = "Pencahue", "Pencahue"
    RIO_CLARO = "Río Claro", "Río Claro"
    SAN_CLEMENTE = "San Clemente", "San Clemente"
    SAN_RAFAEL = "San Rafael", "San Rafael"
    CAUQUENES = "Cauquenes", "Cauquenes"
    CHANCO = "Chanco", "Chanco"
    PELLUHUE = "Pelluhue", "Pelluhue"
    CURICO = "Curicó", "Curicó"
    HUALANE = "Hualañé", "Hualañé"
    LICANTEN = "Licantén", "Licantén"
    MOLINA = "Molina", "Molina"
    RAUCO = "Rauco", "Rauco"
    ROMERAL = "Romeral", "Romeral"
    SAGRADA_FAMILIA = "Sagrada Familia", "Sagrada Familia"
    TENO = "Teno", "Teno"
    VICHUQUEN = "Vichuquén", "Vichuquén"
    LINARES = "Linares", "Linares"
    COLBUN = "Colbún", "Colbún"
    LONGAVI = "Longaví", "Longaví"
    PARRAL = "Parral", "Parral"
    RETIRO = "Retiro", "Retiro"
    SAN_JAVIER = "San Javier", "San Javier"
    VILLA_ALEGRE = "Villa Alegre", "Villa Alegre"
    YERBAS_BUENAS = "Yerbas Buenas", "Yerbas Buenas"
    COBQUECURA = "Cobquecura", "Cobquecura"
    COELEMU = "Coelemu", "Coelemu"
    NINHUE = "Ninhue", "Ninhue"
    PORTEZUELO = "Portezuelo", "Portezuelo"
    QUIRIHUE = "Quirihue", "Quirihue"
    RANQUIL = "Ránquil", "Ránquil"
    TREGUACO = "Treguaco", "Treguaco"
    BULNES = "Bulnes", "Bulnes"
    CHILLAN_VIEJO = "Chillán Viejo", "Chillán Viejo"
    CHILLAN = "Chillán", "Chillán"
    EL_CARMEN = "El Carmen", "El Carmen"
    PEMUCO = "Pemuco", "Pemuco"
    PINTO = "Pinto", "Pinto"
    QUILLON = "Quillón", "Quillón"
    SAN_IGNACIO = "San Ignacio", "San Ignacio"
    YUNGAY = "Yungay", "Yungay"
    COIHUECO = "Coihueco", "Coihueco"
    NIQUEN = "Ñiquén", "Ñiquén"
    SAN_CARLOS = "San Carlos", "San Carlos"
    SAN_FABIAN = "San Fabián", "San Fabián"
    SAN_NICOLAS = "San Nicolás", "San Nicolás"
    CONCEPCION = "Concepción", "Concepción"
    CORONEL = "Coronel", "Coronel"
    CHIGUAYANTE = "Chiguayante", "Chiguayante"
    FLORIDA = "Florida", "Florida"
    HUALQUI = "Hualqui", "Hualqui"
    LOTA = "Lota", "Lota"
    PENCO = "Penco", "Penco"
    SAN_PEDRO_DE_LA_PAZ = "San Pedro de la Paz", "San Pedro de la Paz"
    SANTA_JUANA = "Santa Juana", "Santa Juana"
    TALCAHUANO = "Talcahuano", "Talcahuano"
    TOME = "Tomé", "Tomé"
    HUALPEN = "Hualpén", "Hualpén"
    LEBU = "Lebu", "Lebu"
    ARAUCO = "Arauco", "Arauco"
    CANETE = "Cañete", "Cañete"
    CONTULMO = "Contulmo", "Contulmo"
    CURANILAHUE = "Curanilahue", "Curanilahue"
    LOS_ALAMOS = "Los Álamos", "Los Álamos"
    TIRUA = "Tirúa", "Tirúa"
    LOS_ANGELES = "Los Ángeles", "Los Ángeles"
    ANTUCO = "Antuco", "Antuco"
    CABRERO = "Cabrero", "Cabrero"
    LAJA = "Laja", "Laja"
    MULCHEN = "Mulchén", "Mulchén"
    NACIMIENTO = "Nacimiento", "Nacimiento"
    NEGRETE = "Negrete", "Negrete"
    QUILACO = "Quilaco", "Quilaco"
    QUILLECO = "Quilleco", "Quilleco"
    SAN_ROSENDO = "San Rosendo", "San Rosendo"
    SANTA_BARBARA = "Santa Bárbara", "Santa Bárbara"
    TUCAPEL = "Tucapel", "Tucapel"
    YUMBEL = "Yumbel", "Yumbel"
    ALTO_BIOBIO = "Alto Biobío", "Alto Biobío"
    TEMUCO = "Temuco", "Temuco"
    CARAHUE = "Carahue", "Carahue"
    CUNCO = "Cunco", "Cunco"
    CURARREHUE = "Curarrehue", "Curarrehue"
    FREIRE = "Freire", "Freire"
    GALVARINO = "Galvarino", "Galvarino"
    GORBEA = "Gorbea", "Gorbea"
    LAUTARO = "Lautaro", "Lautaro"
    LONCOCHE = "Loncoche", "Loncoche"
    MELIPEUCO = "Melipeuco", "Melipeuco"
    NUEVA_IMPERIAL = "Nueva Imperial", "Nueva Imperial"
    PADRE_LAS_CASAS = "Padre las Casas", "Padre las Casas"
    PERQUENCO = "Perquenco", "Perquenco"
    PITRUFQUEN = "Pitrufquén", "Pitrufquén"
    PUCON = "Pucón", "Pucón"
    SAAVEDRA = "Saavedra", "Saavedra"
    TEODORO_SCHMIDT = "Teodoro Schmidt", "Teodoro Schmidt"
    TOLTEN = "Toltén", "Toltén"
    VILCUN = "Vilcún", "Vilcún"
    VILLARRICA = "Villarrica", "Villarrica"
    CHOLCHOL = "Cholchol", "Cholchol"
    ANGOL = "Angol", "Angol"
    COLLIPULLI = "Collipulli", "Collipulli"
    CURACAUTIN = "Curacautín", "Curacautín"
    ERCILLA = "Ercilla", "Ercilla"
    LONQUIMAY = "Lonquimay", "Lonquimay"
    LOS_SAUCES = "Los Sauces", "Los Sauces"
    LUMACO = "Lumaco", "Lumaco"
    PUREN = "Purén", "Purén"
    RENAICO = "Renaico", "Renaico"
    TRAIGUEN = "Traiguén", "Traiguén"
    VICTORIA = "Victoria", "Victoria"
    VALDIVIA = "Valdivia", "Valdivia"
    CORRAL = "Corral", "Corral"
    LANCO = "Lanco", "Lanco"
    LOS_LAGOS = "Los Lagos", "Los Lagos"
    MAFIL = "Máfil", "Máfil"
    MARIQUINA = "Mariquina", "Mariquina"
    PAILLACO = "Paillaco", "Paillaco"
    PANGUIPULLI = "Panguipulli", "Panguipulli"
    LA_UNION = "La Unión", "La Unión"
    FUTRONO = "Futrono", "Futrono"
    LAGO_RANCO = "Lago Ranco", "Lago Ranco"
    RIO_BUENO = "Río Bueno", "Río Bueno"
    PUERTO_MONTT = "Puerto Montt", "Puerto Montt"
    CALBUCO = "Calbuco", "Calbuco"
    COCHAMO = "Cochamó", "Cochamó"
    FRESIA = "Fresia", "Fresia"
    FRUTILLAR = "Frutillar", "Frutillar"
    LOS_MUERMOS = "Los Muermos", "Los Muermos"
    LLANQUIHUE = "Llanquihue", "Llanquihue"
    MAULLIN = "Maullín", "Maullín"
    PUERTO_VARAS = "Puerto Varas", "Puerto Varas"
    CASTRO = "Castro", "Castro"
    ANCUD = "Ancud", "Ancud"
    CHONCHI = "Chonchi", "Chonchi"
    CURACO_DE_VELEZ = "Curaco de Vélez", "Curaco de Vélez"
    DALCAHUE = "Dalcahue", "Dalcahue"
    PUQUELDON = "Puqueldón", "Puqueldón"
    QUEILEN = "Queilén", "Queilén"
    QUELLON = "Quellón", "Quellón"
    QUEMCHI = "Quemchi", "Quemchi"
    QUINCHAO = "Quinchao", "Quinchao"
    OSORNO = "Osorno", "Osorno"
    PUERTO_OCTAY = "Puerto Octay", "Puerto Octay"
    PURRANQUE = "Purranque", "Purranque"
    PUYEHUE = "Puyehue", "Puyehue"
    RIO_NEGRO = "Río Negro", "Río Negro"
    SAN_JUAN_DE_LA_COSTA = "San Juan de la Costa", "San Juan de la Costa"
    SAN_PABLO = "San Pablo", "San Pablo"
    CHAITEN = "Chaitén", "Chaitén"
    FUTALEUFU = "Futaleufú", "Futaleufú"
    HUALAIHUE = "Hualaihué", "Hualaihué"
    PALENA = "Palena", "Palena"
    COIHAIQUE = "Coihaique", "Coihaique"
    LAGO_VERDE = "Lago Verde", "Lago Verde"
    AISEN = "Aisén", "Aisén"
    CISNES = "Cisnes", "Cisnes"
    GUAITECAS = "Guaitecas", "Guaitecas"
    COCHRANE = "Cochrane", "Cochrane"
    OHIGGINS = "O’Higgins", "O’Higgins"
    TORTEL = "Tortel", "Tortel"
    CHILE_CHICO = "Chile Chico", "Chile Chico"
    RIO_IBANEZ = "Río Ibáñez", "Río Ibáñez"
    PUNTA_ARENAS = "Punta Arenas", "Punta Arenas"
    LAGUNA_BLANCA = "Laguna Blanca", "Laguna Blanca"
    RIO_VERDE = "Río Verde", "Río Verde"
    SAN_GREGORIO = "San Gregorio", "San Gregorio"
    CABO_DE_HORNOS_ = "Cabo de Hornos (Ex Navarino)", "Cabo de Hornos (Ex Navarino)"
    ANTARTICA = "Antártica", "Antártica"
    PORVENIR = "Porvenir", "Porvenir"
    PRIMAVERA = "Primavera", "Primavera"
    TIMAUKEL = "Timaukel", "Timaukel"
    NATALES = "Natales", "Natales"
    TORRES_DEL_PAINE = "Torres del Paine", "Torres del Paine"
    CERRILLOS = "Cerrillos", "Cerrillos"
    CERRO_NAVIA = "Cerro Navia", "Cerro Navia"
    CONCHALI = "Conchalí", "Conchalí"
    EL_BOSQUE = "El Bosque", "El Bosque"
    ESTACION_CENTRAL = "Estación Central", "Estación Central"
    HUECHURABA = "Huechuraba", "Huechuraba"
    INDEPENDENCIA = "Independencia", "Independencia"
    LA_CISTERNA = "La Cisterna", "La Cisterna"
    LA_FLORIDA = "La Florida", "La Florida"
    LA_GRANJA = "La Granja", "La Granja"
    LA_PINTANA = "La Pintana", "La Pintana"
    LA_REINA = "La Reina", "La Reina"
    LAS_CONDES = "Las Condes", "Las Condes"
    LO_BARNECHEA = "Lo Barnechea", "Lo Barnechea"
    LO_ESPEJO = "Lo Espejo", "Lo Espejo"
    LO_PRADO = "Lo Prado", "Lo Prado"
    MACUL = "Macul", "Macul"
    MAIPU = "Maipú", "Maipú"
    NUNOA = "Ñuñoa", "Ñuñoa"
    PEDRO_AGUIRRE_CERDA = "Pedro Aguirre Cerda", "Pedro Aguirre Cerda"
    PENALOLEN = "Peñalolén", "Peñalolén"
    PROVIDENCIA = "Providencia", "Providencia"
    PUDAHUEL = "Pudahuel", "Pudahuel"
    QUILICURA = "Quilicura", "Quilicura"
    QUINTA_NORMAL = "Quinta Normal", "Quinta Normal"
    RECOLETA = "Recoleta", "Recoleta"
    RENCA = "Renca", "Renca"
    SANTIAGO = "Santiago", "Santiago"
    SAN_JOAQUIN = "San Joaquín", "San Joaquín"
    SAN_MIGUEL = "San Miguel", "San Miguel"
    SAN_RAMON = "San Ramón", "San Ramón"
    VITACURA = "Vitacura", "Vitacura"
    PUENTE_ALTO = "Puente Alto", "Puente Alto"
    PIRQUE = "Pirque", "Pirque"
    SAN_JOSE_DE_MAIPO = "San José de Maipo", "San José de Maipo"
    COLINA = "Colina", "Colina"
    LAMPA = "Lampa", "Lampa"
    TILTIL = "Tiltil", "Tiltil"
    SAN_BERNARDO = "San Bernardo", "San Bernardo"
    BUIN = "Buin", "Buin"
    CALERA_DE_TANGO = "Calera de Tango", "Calera de Tango"
    PAINE = "Paine", "Paine"
    MELIPILLA = "Melipilla", "Melipilla"
    ALHUE = "Alhué", "Alhué"
    CURACAVI = "Curacaví", "Curacaví"
    MARIA_PINTO = "María Pinto", "María Pinto"
    SAN_PEDRO = "San Pedro", "San Pedro"
    TALAGANTE = "Talagante", "Talagante"
    EL_MONTE = "El Monte", "El Monte"
    ISLA_DE_MAIPO = "Isla de Maipo", "Isla de Maipo"
    PADRE_HURTADO = "Padre Hurtado", "Padre Hurtado"
    PENAFLOR = "Peñaflor", "Peñaflor"


class RegionChoices (models.TextChoices):
    AISEN_DEL_GENERAL_CARLOS_IBANEZ_DEL_CAMPO = "Aisén del General Carlos Ibáñez del Campo", "Aisén del General Carlos Ibáñez del Campo"
    ANTOFAGASTA = "Antofagasta", "Antofagasta"
    ARAUCANIA = "La Araucanía", "La Araucanía"
    ARICA_Y_PARINACOTA = "Arica y Parinacota", "Arica y Parinacota"
    ATACAMA = "Atacama", "Atacama"
    BIOBIO = "Biobío", "Biobío"
    COQUIMBO = "Coquimbo", "Coquimbo"
    LIBERTADOR_GENERAL_BERNARDO_OHIGGINS = "Libertador General Bernardo O'Higgins", "Libertador General Bernardo O'Higgins"
    LOS_LAGOS = "Los Lagos", "Los Lagos"
    LOS_RIOS = "Los Ríos", "Los Ríos"
    MAGALLANES_Y_LA_ANTARTICA_CHILENA = "Magallanes y la Antártica Chilena", "Magallanes y la Antártica Chilena"
    MAULE = "Maule", "Maule"
    METROPOLITANA_DE_SANTIAGO = "Metropolitana de Santiago", "Metropolitana de Santiago"
    NUBLE = "Ñuble", "Ñuble"
    TARAPACA = "Tarapacá", "Tarapacá"
    VALPARAISO = "Valparaíso", "Valparaíso"

class Region (models.Model):
    nombre_region = models.CharField(choices = RegionChoices.choices, default = RegionChoices.METROPOLITANA_DE_SANTIAGO, null = False, blank= False, max_length = 50,verbose_name = 'Region')

    def __str__(self):
        return f'{self.nombre_region}'

class Comuna (models.Model):
    nombre_comuna = models.CharField(choices=ComunaChoices.choices, default = ComunaChoices.SANTIAGO, null = False, blank= False, max_length = 50,verbose_name = 'Comuna')
    region = models.ForeignKey(to= Region, on_delete = models.CASCADE, null=True, verbose_name="Region")
            
    def __str__(self):
        return f'{self.nombre_comuna}'

class TipoUsuarioChoices (models.TextChoices):
    ARRENDATARIO = "arrendatario", "arrendatario"
    ARRENDADOR = "arrendador", "arrendador"

class TipoUsuario (models.Model):
    nombre_tipo_usuario = models.CharField(choices = TipoUsuarioChoices.choices, default = TipoUsuarioChoices.ARRENDADOR, null = False, blank= False, max_length = 50,verbose_name = 'Tipo de Usuario')
        
    def __str__(self):
        return f'{self.nombre_tipo_usuario}'

class TipoInmuebleChoices (models.TextChoices):
    CASA = "Casa", "Casa"
    DEPARTAMENTO = "Departamento", "Departamento"
    PARCELA = "Parcela", "Parcela"

class TipoInmueble (models.Model):
    nombre_tipo_inmueble = models.CharField(choices = TipoInmuebleChoices.choices, default = TipoInmuebleChoices.CASA, null = False, blank= False, max_length = 50,verbose_name = 'Tipo de Inmueble')

    def __str__(self):
        return f'{self.nombre_tipo_inmueble}'

class ContactRequest(models.Model):
    customer_email = models.EmailField(verbose_name = "Correo Electronico")
    customer_name = models.CharField(max_length=64, verbose_name="Nombre")
    message = models.TextField(verbose_name="Mensaje")
