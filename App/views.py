from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import AmenazaForm, UsuarioForm
from .models import Amenaza, Usuario
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from .decorators import usuario_login_requerido, rol_requerido
from .models import Amenaza, Especie, Denuncia, Avistamiento
from django.db.models import Count
from .forms import EspecieForm
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import random


# ============================================================
#                        HOME
# ============================================================
def home(request):
    amenazas = Amenaza.objects.all()
    amenaza_dia = random.choice(amenazas) if amenazas else None

    ranking_especies = [
        {"nombre": "Picaflor de Arica", "estado": "En Peligro Crítico", "imagen": ""},
        {"nombre": "Huemul", "estado": "En Peligro",
         "imagen": "https://upload.wikimedia.org/wikipedia/commons/5/53/Huemul_%28Hippocamelus_bisulcus%29.jpg"},
        {"nombre": "Gato Andino", "estado": "En Peligro",
         "imagen": "https://upload.wikimedia.org/wikipedia/commons/d/d0/Leopardus_jacobita_2.jpg"},
        {"nombre": "Rana Chilena", "estado": "Vulnerable", "imagen": "ranaChilena.jpg"},
        {"nombre": "Ranita de Darwin", "estado": "En Peligro",
         "imagen": "https://upload.wikimedia.org/wikipedia/commons/c/cb/Chiloe_Wudl_2.jpg"},
        {"nombre": "Puma", "estado": "Preocupación menor",
         "imagen": "https://upload.wikimedia.org/wikipedia/commons/8/8c/Puma_concolor_-_Ravine_Hall_-_Chester_Zoo%2C_England.jpg"},
        {"nombre": "Cóndor Andino", "estado": "Casi amenazado",
         "imagen": "https://upload.wikimedia.org/wikipedia/commons/1/1d/Condor_peru.jpg"},
        {"nombre": "Pudú", "estado": "Vulnerable",
         "imagen": "https://upload.wikimedia.org/wikipedia/commons/3/3c/Pudu_pudu.jpg"},
        {"nombre": "Zorro Culpeo", "estado": "Preocupación menor",
         "imagen": "https://upload.wikimedia.org/wikipedia/commons/0/0f/Lycalopex_culpeus_%28Zorro_Culpeo%29.jpg"},
        {"nombre": "Chungungo", "estado": "En Peligro",
         "imagen": "https://upload.wikimedia.org/wikipedia/commons/3/35/Lontra_felina.jpg"},
    ]

    return render(request, "home.html", {
        "amenaza_dia": amenaza_dia,
        "ranking": ranking_especies
    })


# ============================================================
#                REGISTRO / LOGIN / LOGOUT
# ============================================================
def signup(request):
    if request.method == 'GET':
        form = UsuarioForm()
        return render(request, 'signup.html', {'form': form})
    else:
        form = UsuarioForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Usuario registrado correctamente.')
                return redirect('logearse')
            except IntegrityError:
                return render(request, 'signup.html', {'form': form, 'error': 'Correo ya registrado.'})
        return render(request, 'signup.html', {'form': form, 'error': 'Datos inválidos.'})


def logearse(request):
    if request.method == 'GET':
        return render(request, 'logearse.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(password, usuario.hash_password):

                request.session['usuario_id'] = usuario.usuario_id
                request.session['usuario_nombre'] = usuario.nombre
                request.session['usuario_rol'] = usuario.rol
                request.session.set_expiry(900)

                return redirect('amenazas')
            else:
                return render(request, 'logearse.html', {'error': 'Contraseña incorrecta.'})

        except Usuario.DoesNotExist:
            return render(request, 'logearse.html', {'error': 'Correo no registrado.'})


def signout(request):
    request.session.flush()
    return redirect('home')


# ============================================================
#                      AMENAZAS
# ============================================================
@usuario_login_requerido
def amenazas(request):
    threat = Amenaza.objects.all()
    return render(request, "amenazas.html", {'amenazas': threat})


# Usuario normal, investigador y admin pueden crear amenazas
@usuario_login_requerido
@rol_requerido(["Usuario", "Investigador", "Administrador"])
def create_amenaza(request):
    if request.method == "GET":
        return render(request, "crear_amenaza.html", {"form": AmenazaForm})
    else:
        form = AmenazaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('amenazas')
        return render(request, "crear_amenaza.html", {"form": AmenazaForm, "error": "Error al crear."})


@usuario_login_requerido
def amenaza_detail(request, amenaza_id):
    threat = get_object_or_404(Amenaza, pk=amenaza_id)
    return render(request, 'amenaza_detail.html', {'threat': threat})


# Investigador y admin pueden editar
@usuario_login_requerido
@rol_requerido(["Investigador", "Administrador"])
def amenaza_edit(request, amenaza_id):
    amenaza = get_object_or_404(Amenaza, pk=amenaza_id)

    if request.method == 'GET':
        form = AmenazaForm(instance=amenaza)
        return render(request, 'editar_amenaza.html', {'form': form, 'amenaza': amenaza})

    form = AmenazaForm(request.POST, instance=amenaza)
    if form.is_valid():
        form.save()
        return redirect('amenaza_detail', amenaza_id=amenaza.amenaza_id)

    return render(request, 'editar_amenaza.html', {'form': form, 'amenaza': amenaza, 'error': 'Error al actualizar.'})


# Investigador y admin pueden eliminar
@usuario_login_requerido
@rol_requerido(["Investigador", "Administrador"])
def amenaza_eliminar(request, amenaza_id):
    amenaza = get_object_or_404(Amenaza, pk=amenaza_id)
    if request.method == "POST":
        amenaza.delete()
        return redirect('amenazas')
    return render(request, 'eliminar_amenaza.html', {'amenaza': amenaza})


# ============================================================
#                    PÁGINA EDUCATIVA
# ============================================================
@usuario_login_requerido
def educativo(request):
    return render(request, 'educacion.html')


# ============================================================
#                      DASHBOARD
# ============================================================
@usuario_login_requerido
def dashboard(request):
    total_amenazas = Amenaza.objects.count()
    total_especies = Especie.objects.count()
    total_denuncias = Denuncia.objects.count()
    total_avistamientos = Avistamiento.objects.count()

    tipos = list(Amenaza.objects.values_list('tipo', flat=True).distinct())
    cantidades = [Amenaza.objects.filter(tipo=t).count() for t in tipos]

    context = {
        'total_amenazas': total_amenazas,
        'total_especies': total_especies,
        'total_denuncias': total_denuncias,
        'total_avistamientos': total_avistamientos,
        'tipos_amenaza': json.dumps(tipos),
        'cantidad_por_tipo': json.dumps(cantidades),
    }

    return render(request, 'dashboard.html', context)


# ============================================================
#                         MAPA
# ============================================================
@usuario_login_requerido
def mapa_amenazas(request):
    amenazas = Amenaza.objects.all().values("nombre", "tipo", "descripcion", "lat", "lon")
    return render(request, "mapa.html", {"amenazas_json": json.dumps(list(amenazas))})


# ============================================================
#                        ESPECIES
# ============================================================
@usuario_login_requerido
def especies_list(request):
    especies = Especie.objects.all()
    return render(request, "especies.html", {"especies": especies})


@usuario_login_requerido
def especie_detail(request, especie_id):
    especie = get_object_or_404(Especie, pk=especie_id)
    return render(request, "especie_detail.html", {"especie": especie})


# Investigador y admin pueden crear especies
@usuario_login_requerido
@rol_requerido(["Investigador", "Administrador"])
def especie_create(request):
    if request.method == "GET":
        form = EspecieForm()
        return render(request, "especie_form.html", {"form": form, "title": "Registrar Especie", "button": "Guardar"})

    form = EspecieForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect("especies")

    return render(request, "especie_form.html", {"form": form, "title": "Registrar Especie", "button": "Guardar",
                                                 "error": "Error al guardar."})


# Investigador y admin pueden editar especies
@usuario_login_requerido
@rol_requerido(["Investigador", "Administrador"])
def especie_edit(request, especie_id):
    especie = get_object_or_404(Especie, pk=especie_id)

    if request.method == "GET":
        form = EspecieForm(instance=especie)
        return render(request, "especie_form.html", {"form": form, "title": "Editar Especie", "button": "Actualizar",
                                                     "especie": especie})

    form = EspecieForm(request.POST, instance=especie)
    if form.is_valid():
        form.save()
        return redirect("especie_detail", especie_id=especie.especie_id)

    return render(request, "especie_form.html",
                  {"form": form, "title": "Editar Especie", "button": "Actualizar",
                   "especie": especie, "error": "Error al actualizar."})


# Investigador y admin pueden eliminar especies
@usuario_login_requerido
@rol_requerido(["Investigador", "Administrador"])
def especie_delete(request, especie_id):
    especie = get_object_or_404(Especie, pk=especie_id)

    if request.method == "POST":
        especie.delete()
        return redirect("especies")

    return render(request, "especie_delete_confirm.html", {"especie": especie})


# ============================================================
#           GBIF / INATURALIST (SIN CAMBIOS)
# ============================================================
@usuario_login_requerido
def gbif_especie(request):
    nombre = request.GET.get("q", None)
    datos = None
    ocurrencias = None

    if nombre:
        url = f"https://api.gbif.org/v1/species/search?q={nombre}&rank=species"
        response = requests.get(url).json()

        if response["results"]:
            especie = response["results"][0]

            imagen = None
            media = requests.get(f"https://api.gbif.org/v1/species/{especie.get('key')}/media").json()
            if media:
                imagen = media[0].get("identifier")

            datos = {
                "nombre_cientifico": especie.get("scientificName"),
                "reino": especie.get("kingdom"),
                "familia": especie.get("family"),
                "autor": especie.get("authorship"),
                "key": especie.get("key"),
                "imagen": imagen,
            }

            occ_resp = requests.get(f"https://api.gbif.org/v1/occurrence/search?speciesKey={especie['key']}").json()
            ocurrencias = occ_resp.get("results", [])[:10]

    return render(request, "gbif_especie.html", {"datos": datos, "ocurrencias": ocurrencias, "query": nombre})


@usuario_login_requerido
def inaturalist_buscar(request):
    nombre = request.GET.get("q", None)

    observaciones = []
    mapa_data = []
    stats = None

    if nombre:
        url = (
            "https://api.inaturalist.org/v1/observations"
            f"?taxon_name={nombre}&per_page=50&place_code=CL"
        )

        response = requests.get(url, verify=False).json()
        observaciones = response.get("results", [])

        for obs in observaciones:
            foto = None
            if obs.get("photos"):
                foto = obs["photos"][0]["url"].replace("square", "large")

            if obs.get("geojson"):
                mapa_data.append({
                    "lat": obs["geojson"]["coordinates"][1],
                    "lon": obs["geojson"]["coordinates"][0],
                    "foto": foto,
                    "nombre": obs["taxon"]["name"] if obs.get("taxon") else nombre,
                    "fecha": obs.get("observed_on_details", {}).get("date", "N/A")
                })

        stats = {
            "total_obs": len(observaciones),
            "con_foto": len([o for o in observaciones if o.get("photos")]),
            "con_geo": len(mapa_data),
        }

    return render(request, "inaturalist_buscar.html", {
        "observaciones": observaciones,
        "mapa_data": json.dumps(mapa_data),
        "stats": stats,
        "query": nombre
    })


# ============================================================
#                 ADMINISTRACIÓN DE USUARIOS
# ============================================================
@usuario_login_requerido
@rol_requerido("Administrador")
def usuarios_list(request):
    usuarios = Usuario.objects.all()
    return render(request, "admin_usuarios_list.html", {'usuarios': usuarios})


@usuario_login_requerido
@rol_requerido("Administrador")
def usuarios_create(request):
    if request.method == 'GET':
        form = UsuarioForm()
        return render(request, "admin_usuarios_form.html", {'form': form, 'title': "Crear Usuario"})

    form = UsuarioForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('usuarios_list')

    return render(request, "admin_usuarios_form.html",
                  {'form': form, 'title': "Crear Usuario", 'error': 'Datos inválidos'})


@usuario_login_requerido
@rol_requerido("Administrador")
def usuarios_edit(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)

    if request.method == 'GET':
        form = UsuarioForm(instance=usuario)
        return render(request, "admin_usuarios_form.html", {'form': form, 'title': "Editar Usuario"})

    form = UsuarioForm(request.POST, instance=usuario)
    if form.is_valid():
        form.save()
        return redirect('usuarios_list')

    return render(request, "admin_usuarios_form.html",
                  {'form': form, 'title': "Editar Usuario", 'error': 'Datos inválidos'})


@usuario_login_requerido
@rol_requerido("Administrador")
def usuarios_delete(request, user_id):
    usuario = get_object_or_404(Usuario, pk=user_id)

    if request.method == 'POST':
        usuario.delete()
        return redirect('usuarios_list')

    return render(request, "admin_usuarios_delete.html", {'usuario': usuario})


@usuario_login_requerido
@rol_requerido("Administrador")
def panel_admin(request):
    return render(request, "panel_admin.html")


@usuario_login_requerido
@rol_requerido("Administrador")
def cambiar_rol(request, usuario_id):
    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if request.method == "POST":
        nuevo_rol = request.POST.get("rol")

        if nuevo_rol in ["Administrador", "Investigador", "Usuario"]:
            usuario.rol = nuevo_rol
            usuario.save()
            return redirect("usuarios_list")

        return render(request, "cambiar_rol.html", {"usuario": usuario, "error": "Rol inválido"})

    return render(request, "cambiar_rol.html", {"usuario": usuario})
