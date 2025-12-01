from django.db import models
from django.contrib.auth.hashers import make_password, check_password

# === Región y Comuna ===
class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(unique=True, max_length=10)

    class Meta:
        db_table = 'region'

    def __str__(self):
        return self.nombre


class Comuna(models.Model):
    comuna_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    region = models.ForeignKey(Region, models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'comuna'

    def __str__(self):
        return self.nombre


# === Usuario ===
class Usuario(models.Model):
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Investigador', 'Investigador'),
        ('Usuario', 'Usuario'),
    ]

    usuario_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    email = models.CharField(unique=True, max_length=150)
    hash_password = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES)
    comuna = models.ForeignKey('Comuna', models.DO_NOTHING, null=True, blank=True)
    verificado = models.BooleanField(default=False)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario'

    def __str__(self):
        return f"{self.nombre} ({self.rol})"

# === Ecosistema ===
class Ecosistema(models.Model):
    ecosistema_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=140)
    tipo = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    region = models.ForeignKey(Region, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        db_table = 'ecosistema'

    def __str__(self):
        return self.nombre


# === Amenaza ===
class Amenaza(models.Model):
    TIPO_CHOICES = [
        ('Contaminación', 'Contaminación'),
        ('Deforestación', 'Deforestación'),
        ('Caza furtiva', 'Caza furtiva'),
        ('Cambio climático', 'Cambio climático'),
        ('Especies invasoras', 'Especies invasoras'),
        ('Otro', 'Otro'),
    ]

    amenaza_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(max_length=80, choices=TIPO_CHOICES)
    descripcion = models.TextField(blank=True, null=True)

    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lon = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)



    class Meta:
        db_table = 'amenaza'

    #def __str__(self):
        #return str(self.amenaza_id) + " " + self.nombre + " " + str(self.tipo) + " " + " " + str(self.descripcion) + ")"
    #def __str__(self):
    #    return str(self.amenaza_id) + " " + self.nombre + "($" + str(self.tipo) + ")" + "($" + str(self.descripcion) + ")" 
# === Especie ===
class Especie(models.Model):
    especie_id = models.AutoField(primary_key=True)
    nombre_cientifico = models.CharField(unique=True, max_length=160)
    nombre_comun = models.CharField(max_length=160, blank=True, null=True)
    grupo_taxonomico = models.CharField(max_length=80)
    endemica = models.BooleanField(default=False)
    foto_url = models.CharField(max_length=250, blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'especie'

    def __str__(self):
        return self.nombre_cientifico


# === Relaciones entre especies ===
class EspecieAmenaza(models.Model):
    id = models.AutoField(primary_key=True)
    especie = models.ForeignKey(Especie, models.DO_NOTHING, null=True, blank=True)
    amenaza = models.ForeignKey(Amenaza, models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'especie_amenaza'


class EspecieEcosistema(models.Model):
    id = models.AutoField(primary_key=True)
    especie = models.ForeignKey(Especie, models.DO_NOTHING, null=True, blank=True)
    ecosistema = models.ForeignKey(Ecosistema, models.DO_NOTHING, null=True, blank=True)

    class Meta:
        db_table = 'especie_ecosistema'


# === Avistamiento ===
class Avistamiento(models.Model):
    avistamiento_id = models.AutoField(primary_key=True)
    especie = models.ForeignKey(Especie, models.DO_NOTHING, null=True, blank=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, null=True, blank=True)
    fecha_hora = models.DateTimeField()
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    precision_m = models.IntegerField(blank=True, null=True)
    metodo = models.CharField(max_length=80, blank=True, null=True)
    evidencia_url = models.CharField(max_length=250, blank=True, null=True)
    estado = models.CharField(max_length=12)
    validado_por = models.ForeignKey(
        Usuario,
        models.DO_NOTHING,
        db_column='validado_por',
        related_name='avistamientos_validados',
        blank=True,
        null=True
    )
    notas = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'avistamiento'


# === Denuncia ===
class Denuncia(models.Model):
    denuncia_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuario, models.DO_NOTHING, null=True, blank=True)
    tipo = models.CharField(max_length=20)
    descripcion = models.TextField()
    fecha_hora = models.DateTimeField(auto_now_add=True)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lon = models.DecimalField(max_digits=9, decimal_places=6)
    estado = models.CharField(max_length=20)
    autoridad_derivada = models.CharField(max_length=160, blank=True, null=True)
    folio_externo = models.CharField(max_length=80, blank=True, null=True)
    evidencia_url = models.CharField(max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'denuncia'
