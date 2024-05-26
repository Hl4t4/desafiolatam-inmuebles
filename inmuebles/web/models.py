from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator 
from web.validators import TipoUsuarioValidator
from datetime import date


# Create your models here.


class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Se debe usar un correo electronico')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)

class Usuario (AbstractBaseUser, PermissionsMixin):
    class TipoUsuario (models.TextChoices):
        ARRENDATARIO = "arrendatario", "arrendatario"
        ARRENDADOR = "arrendador", "arrendador"
    email = models.EmailField(unique = True, null = False, blank = False, verbose_name = 'Correo Electronico')
    nombres = models.CharField(max_length = 50, null = False, blank = False, verbose_name = 'Nombres')
    apellidos = models.CharField(max_length = 50, null = False, blank = False, verbose_name = 'Apellidos')
    rut = models.CharField(max_length = 10, null = False, blank = False, verbose_name = 'RUT')
    direccion = models.CharField(max_length = 50, null = False, blank = True, verbose_name = 'Direccion')
    telefono_personal = models.IntegerField(null = False, blank = True, verbose_name = 'Telefono Personal')
    tipo_de_usuario = models.CharField(choices = TipoUsuario.choices, default = TipoUsuario.ARRENDADOR)
    #correo_electronico esta como base en abstractuser como email
    is_staff = models.BooleanField(default = False)
    date_joined = models.DateTimeField(auto_now_add = date.today())
    USERNAME_FIELD = 'email'

    objects = UsuarioManager()

    REQUIRED_FIELDS =['nombres', 'apellidos', 'rut', 'direccion', 'telefono_personal', 'tipo_de_usuario']

    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_active(self):
        return True

    def __str__(self):
        return f'Nombre: {self.nombres} {self.apellidos}\n RUT: {self.rut}\n Direccion: {self.direccion}, Telefono: {self.telefono_personal}\n Correo Electronico: {self.email}\n Tipo de Usuario: {self.tipo_de_usuario}'

    # def __init__(self, nombres:str, apellido:str, rut:str, direccion:str, telefono_personal:str, tipo_de_usuario:str, *args: Any, **kwargs: Any) -> None:
    #     super().__init__(*args, **kwargs)


class Inmueble (models.Model):
    class TipoInmueble (models.TextChoices):
        CASA = "Casa", "Casa"
        DEPARTAMENTO = "Departamento", "Departamento"
        PARCELA = "Parcela", "Parcela"
    class Comuna (models.TextChoices):
        SANTIAGO = "Santiago", "Santiago"
        LA_FLORIDA = "La Florida", "La Florida"
        MAIPU = "Maipú", "Maipú"
        LAS_CONDES = "Las Condes", "Las Condes"
        PUENTE_ALTO = "Puente Alto", "Puente Alto"
        SAN_BERNARDO = "San Bernardo", "San Bernardo"
        LA_PINTANA = "La Pintana", "La Pintana"
        QUILICURA = "Quilicura", "Quilicura"
        RECOLETA = "Recoleta", "Recoleta"
        PROVIDENCIA = "Providencia", "Providencia"
        LA_REINA = "La Reina", "La Reina"
        PENAFLOR = "Peñaflor", "Peñaflor"
        RENCA = "Renca", "Renca"
        SAN_RAMON = "San Ramón", "San Ramón"
        NUNOA = "Ñuñoa", "Ñuñoa"
        EL_BOSQUE = "El Bosque", "El Bosque"
        INDEPENDENCIA = "Independencia", "Independencia"
        HUECHURABA = "Huechuraba", "Huechuraba"
        COLINA = "Colina", "Colina"
        PADRE_HURTADO = "Padre Hurtado", "Padre Hurtado"
        LO_BARNECHEA = "Lo Barnechea", "Lo Barnechea"
        LO_ESPEJO = "Lo Espejo", "Lo Espejo"
        LO_PRADO = "Lo Prado", "Lo Prado"
        MACUL = "Macul", "Macul"
        CONCHALI = "Conchalí", "Conchalí"
        CERRILLOS = "Cerrillos", "Cerrillos"
        CERRO_NAVIA = "Cerro Navia", "Cerro Navia"
        ESTACION_CENTRAL = "Estación Central", "Estación Central"
        PEDRO_AGUIRRE_CERDA = "Pedro Aguirre Cerda", "Pedro Aguirre Cerda"
        PENALOLEN = "Peñalolén", "Peñalolén"
        PIRQUE = "Pirque", "Pirque"
        SAN_JOAQUIN = "San Joaquín", "San Joaquín"
        SAN_JOSE_DE_MAIPO = "San José de Maipo", "San José de Maipo"
        SAN_MIGUEL = "San Miguel", "San Miguel"
        SANTA_CRUZ = "Santa Cruz", "Santa Cruz"
        TALAGANTE = "Talagante", "Talagante"
        VITACURA = "Vitacura", "Vitacura"
        LA_GRANJA = "La Granja", "La Granja"
        PAINE = "Paine", "Paine"
        ALHUE = "Alhué", "Alhué"
        BUIN = "Buin", "Buin"
        CALERA_DE_TANGO = "Calera de Tango", "Calera de Tango"
        CURACAVI = "Curacaví", "Curacaví"
        LAMPA = "Lampa", "Lampa"
        MARIA_PINTO = "María Pinto", "María Pinto"
        MELIPILLA = "Melipilla", "Melipilla"
        TIL_TIL = "Til Til", "Til Til"
        PUDAGUEL = "Pudahuel", "Pudahuel"
        QUINTA_NORMAL = "Quinta Normal", "Quinta Normal"
        ARICA = "Arica", "Arica"
        CAMARONES = "Camarones", "Camarones"
        GENERAL_LAGOS = "General Lagos", "General Lagos"
        PUTRE = "Putre", "Putre"
        IQUIQUE = "Iquique", "Iquique"
        ALTO_HOSPICIO = "Alto Hospicio", "Alto Hospicio"
        CAMINA = "Camiña", "Camiña"
        COLCHANE = "Colchane", "Colchane"
        HUARA = "Huara", "Huara"
        PICA = "Pica", "Pica"
        POZO_ALMONTE = "Pozo Almonte", "Pozo Almonte"
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
        PUCALAN = "Puchuncaví", "Puchuncaví"
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
        CALERA = "La Calera", "La Calera"
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
        REQUINOA = "Requínoa", "Requínoa"
        RENGO = "Rengo", "Rengo"
        SAN_VICENTE = "San Vicente", "San Vicente"
        PICHILEMU = "Pichilemu", "Pichilemu"
        LA_ESTRELLA = "La Estrella", "La Estrella"
        LITUECHE = "Litueche", "Litueche"
        MARCHIHUE = "Marchihue", "Marchihue"
        NAVIDAD = "Navidad", "Navidad"
        PAREDONES = "Paredones", "Paredones"
        SAN_FERNANDO = "San Fernando", "San Fernando"
        CHIMBARONGO = "Chimbarongo", "Chimbarongo"
        LOLOL = "Lolol", "Lolol"
        NANCAGUA = "Nancagua", "Nancagua"
        PALMILLA = "Palmilla", "Palmilla"
        PERALILLO = "Peralillo", "Peralillo"
        PLACILLA = "Placilla", "Placilla"
        PUMANQUE = "Pumanque", "Pumanque"
        CURICO = "Curicó", "Curicó"
        HUALANE = "Hualañé", "Hualañé"
        LICANTEN = "Licantén", "Licantén"
        MOLINA = "Molina", "Molina"
        RAUCO = "Rauco", "Rauco"
        ROMERAL = "Romeral", "Romeral"
        SAGRADA_FAMILIA = "Sagrada Familia", "Sagrada Familia"
        TENO = "Teno", "Teno"
        VICHUQUEN = "Vichuquén", "Vichuquén"
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
        LINARES = "Linares", "Linares"
        COLBUN = "Colbún", "Colbún"
        LONGAVI = "Longaví", "Longaví"
        PARRAL = "Parral", "Parral"
        RETIRO = "Retiro", "Retiro"
        SAN_JAVIER = "San Javier", "San Javier"
        VILLA_ALEGRE = "Villa Alegre", "Villa Alegre"
        YERBAS_BUENAS = "Yerbas Buenas", "Yerbas Buenas"
        CAUQUENES = "Cauquenes", "Cauquenes"
        CHANCO = "Chanco", "Chanco"
        PELLUHUE = "Pelluhue", "Pelluhue"
        CHILLAN = "Chillán", "Chillán"
        BULNES = "Bulnes", "Bulnes"
        COIHUECO = "Coihueco", "Coihueco"
        EL_CARMEN = "El Carmen", "El Carmen"
        PEMUCO = "Pemuco", "Pemuco"
        PINTO = "Pinto", "Pinto"
        QUILLON = "Quillón", "Quillón"
        SAN_IGNACIO = "San Ignacio", "San Ignacio"
        YUNGAY = "Yungay", "Yungay"
        QUERIHUE = "Quirihue", "Quirihue"
        COBQUECURA = "Cobquecura", "Cobquecura"
        NINHUE = "Ninhue", "Ninhue"
        TREGUACO = "Treguaco", "Treguaco"
        SAN_CARLOS = "San Carlos", "San Carlos"
        NUBLE = "Ñuble", "Ñuble"
        SAN_NICOLAS = "San Nicolás", "San Nicolás"
        CONCEPCION = "Concepción", "Concepción"
        CORONEL = "Coronel", "Coronel"
        CHIGUAYANTE = "Chiguayante", "Chiguayante"
        FLORIDA = "Florida", "Florida"
        HUALQUI = "Hualqui", "Hualqui"
        LO_TA = "Lota", "Lota"
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
        QUILLECO = "Quilleco", "Quilleco"
        SAN_ROSENDO = "San Rosendo", "San Rosendo"
        SANTA_BARBARBARA = "Santa Bárbara", "Santa Bárbara"
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
        PADRE_LAS_CASAS = "Padre Las Casas", "Padre Las Casas"
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
        PURANQUE = "Purén", "Purén"
        RENAICO = "Renaico", "Renaico"
        TRAIGUEN = "Traiguén", "Traiguén"
        VICTORIA = "Victoria", "Victoria"
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
        COYHAIQUE = "Coyhaique", "Coyhaique"
        LAGOS_DEL_MONT = "Lagos del Mont", "Lagos del Mont"
        AISEN = "Aysén", "Aysén"
        CISNES = "Cisnes", "Cisnes"
        GUAITECAS = "Guaitecas", "Guaitecas"
        COCHRANE = "Cochrane", "Cochrane"
        O_HIGGINS = "O'Higgins", "O'Higgins"
        TORTEL = "Tortel", "Tortel"
        CHILE_CHICO = "Chile Chico", "Chile Chico"
        RIO_IBANEZ = "Río Ibáñez", "Río Ibáñez"
        PUNTA_ARENAS = "Punta Arenas", "Punta Arenas"
        LAGUNA_BLANCA = "Laguna Blanca", "Laguna Blanca"
        RIO_VERDE = "Río Verde", "Río Verde"
        SAN_GREGORIO = "San Gregorio", "San Gregorio"
        CABO_DE_HORNOS = "Cabo de Hornos", "Cabo de Hornos"
        ANTARCTICA = "Antártica", "Antártica"
        PORVENIR = "Porvenir", "Porvenir"
        PRIMAVERA = "Primavera", "Primavera"
        TIMAUKEL = "Timaukel", "Timaukel"
        NATALES = "Natales", "Natales"
        TORRES_DEL_PAINE = "Torres del Paine", "Torres del Paine"
        COLCHAGUA = "Colchagua", "Colchagua"
        VALDIVIA = "Valdivia", "Valdivia"
    
    nombre = models.CharField(max_length = 50, null = False, blank = False, verbose_name = 'Nombre')
    descripcion = models.TextField(null = False, blank = True, verbose_name = 'Descripcion')
    m2_construidos = models.FloatField(null = False, blank = False, validators=[MinValueValidator(0.0)], verbose_name = 'Metros² Construidos')
    m2_totales = models.FloatField(null = False, blank = False, validators=[MinValueValidator(0.0)], verbose_name = 'Metros² Totales o del terreno')
    estacionamientos = models.IntegerField(null = False, blank = False, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de estacionamientos')
    habitaciones = models.IntegerField(null = False, blank = False, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de habitaciones')
    restrooms = models.IntegerField(null = False, blank = False, validators=[MinValueValidator(0)], verbose_name = 'Cantidad de baños')
    direccion = models.CharField(max_length = 50, null = False, blank = True, verbose_name = 'Direccion')
    comuna = models.CharField(choices = Comuna.choices, default = Comuna.SANTIAGO, verbose_name = 'Comuna')
    tipo_de_inmueble = models.CharField(choices = TipoInmueble.choices, default = TipoInmueble.CASA)
    arriendo = models.IntegerField(null = False, blank = False, validators=[MinValueValidator(0)], verbose_name = 'Precio mensual de arriendo')
    # arrendador = models.ForeignKey(Usuario, null = True, related_name = 'inmueble_arrendador', on_delete = models.PROTECT, validators=[TipoUsuarioValidator(foreing_key_field = 'arrendador', related_field = 'tipo_de_usuario', tipos_de_usuario = ['arrendador'])])
    # arrendatario = models.ForeignKey(Usuario, null = True, related_name = 'inmueble_arrendatario', on_delete = models.PROTECT, validators=[TipoUsuarioValidator(foreing_key_field = 'arrendatario', related_field = 'tipo_de_usuario', tipos_de_usuario = ['arrendatario'])])
    #Alternativa models.PositiveIntegerField
    arrendador = models.ForeignKey(Usuario, null=True, blank=True, on_delete = models.PROTECT, related_name = 'inmueble_arrendador')
    arrendatario = models.ForeignKey(Usuario, on_delete = models.PROTECT, related_name = 'inmueble_arrendatario')
    
    def clean(self):
        validator_arrendador = TipoUsuarioValidator(foreing_key_field = 'arrendador', related_field = 'tipo_de_usuario', tipos_de_usuario = ['arrendador'])
        validator_arrendatario = TipoUsuarioValidator(foreing_key_field = 'arrendatario', related_field = 'tipo_de_usuario', tipos_de_usuario = ['arrendatario'])
        validator_arrendador(self)
        validator_arrendatario(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Nombre: {self.nombre}\n Descripcion: {self.descripcion}\n Metros² Construidos: {self.m2_construidos}[m²]\n Metros Totales o del Terreno: {self.m2_totales}[m²]\n Cantidad de estacionamientos: {self.estacionamientos}\n Cantidad de habitaciones: {self.habitaciones}\n Cantidad de baños: {self.restrooms}\n Direccion: {self.direccion}, {self.comuna}\n Tipo de Inmueble: {self.tipo_de_inmueble}\n Precio mensual de arriendo: ${self.arriendo}'

class SolicitudArriendo (models.Model):
    arrendador = models.OneToOneField(Usuario, on_delete=models.PROTECT, verbose_name = "Arrendador")
    inmueble = models.ForeignKey(Inmueble, on_delete=models.PROTECT, verbose_name = "Inmueble")
    aceptada = models.BooleanField(default = False, null = False)

    def clean(self):
        validator_arrendador = TipoUsuarioValidator(foreing_key_field = 'arrendador', related_field = 'tipo_de_usuario', tipos_de_usuario = ['arrendador'])
        validator_arrendador(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'El arrendador\n{self.arrendador}\n Desea arrendar el inmueble\n{self.inmueble}\n La solicitud se encuentra aceptada: {self.aceptada}'
