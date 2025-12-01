from django.contrib import admin
from .models import Usuario, Amenaza, Especie, Denuncia

class AmenazaAdmin(admin.ModelAdmin):
    readonly_fields = ("amenaza_id", )

admin.site.register(Amenaza, AmenazaAdmin)
admin.site.register(Usuario)
admin.site.register(Especie)
admin.site.register(Denuncia)
