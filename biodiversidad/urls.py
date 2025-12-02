from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    # Django admin (no lo usas, pero debe existir)
    path('dj-admin/', admin.site.urls),

    # Página principal
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    
    # Autenticación
    path('signup/', views.signup, name='signup'),
    path('logearse/', views.logearse, name='logearse'),
    path('logout/', views.signout, name='logout'),

    # Amenazas
    path('amenazas/', views.amenazas, name='amenazas'),
    path('amenazas/create/', views.create_amenaza, name='create_amenaza'),
    path('amenazas/<int:amenaza_id>/', views.amenaza_detail, name='amenaza_detail'),
    path('amenazas/<int:amenaza_id>/editar/', views.amenaza_edit, name='amenaza_edit'),
    path('amenazas/<int:amenaza_id>/eliminar/', views.amenaza_eliminar, name='amenaza_eliminar'),

    # Página educativa
    path('educativo/', views.educativo, name="educativo"),

    # Dashboard 
    path('dashboard/', views.dashboard, name='dashboard'),

    # Mapa
    path('mapa/', views.mapa_amenazas, name='mapa'),

    # Especies
    path('especies/', views.especies_list, name='especies'),
    path('especies/create/', views.especie_create, name='especie_create'),
    path('especies/<int:especie_id>/', views.especie_detail, name='especie_detail'),
    path('especies/<int:especie_id>/edit/', views.especie_edit, name='especie_edit'),
    path('especies/<int:especie_id>/delete/', views.especie_delete, name='especie_delete'),

    # Buscar especies GBIF
    path('gbif/especie/', views.gbif_especie, name='gbif_especie'),

    # iNaturalist
    path('inaturalist/', views.inaturalist_buscar, name='inaturalist_buscar'),

    # TU panel administrativo CUSTOM
    path('panel/', views.panel_admin, name='panel_admin'),

    # CRUD de usuarios EN TU PANEL, NO en Django Admin
    path('panel/usuarios/', views.usuarios_list, name='usuarios_list'),
    path('panel/usuarios/create/', views.usuarios_create, name='usuarios_create'),
    path('panel/usuarios/<int:user_id>/edit/', views.usuarios_edit, name='usuarios_edit'),
    path('panel/usuarios/<int:user_id>/delete/', views.usuarios_delete, name='usuarios_delete'),
    path('panel/usuarios/<int:usuario_id>/rol/', views.cambiar_rol, name='cambiar_rol'),
]
