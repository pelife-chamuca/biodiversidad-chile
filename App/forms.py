from django.forms import ModelForm
from django import forms
from .models import Amenaza
from .models import Usuario
from django.contrib.auth.hashers import make_password
from .models import Especie


class AmenazaForm(ModelForm):
    class Meta:
        model = Amenaza
        fields = ["amenaza_id", "nombre", "tipo", "descripcion"]


class UsuarioForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")

    class Meta:
        model = Usuario
        fields = ["nombre", "email", "password", "comuna"]


    def save(self, commit=True):
        usuario = super().save(commit=False)

        usuario.hash_password = make_password(self.cleaned_data["password"])

        # Blindaje: un usuario nunca puede crearse como Admin o Investigador
        usuario.rol = "Usuario"

        if commit:
            usuario.save()
        return usuario


class EspecieForm(forms.ModelForm):
    class Meta:
        model = Especie
        fields = [
            "nombre_cientifico",
            "nombre_comun",
            "grupo_taxonomico",
            "foto_url",
            "descripcion",
        ]
