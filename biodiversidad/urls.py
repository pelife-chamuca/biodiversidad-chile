from django.contrib import admin
from django.urls import path
from App import views

urlpatterns = [
    path('admin/', admin.site.urls),
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

    #Pagina dashboard 
    path('dashboard/', views.dashboard, name='dashboard'),

    #Mapa
    path('mapa/', views.mapa_amenazas, name='mapa'),

   
    # ESPECIES
    path('especies/', views.especies_list, name='especies'),
    path('especies/create/', views.especie_create, name='especie_create'),
    path('especies/<int:especie_id>/', views.especie_detail, name='especie_detail'),
    path('especies/<int:especie_id>/edit/', views.especie_edit, name='especie_edit'),

    #PARA BUSCAR ESPECIES GBIF
    path('gbif/especie/', views.gbif_especie, name='gbif_especie'),

    #Integracion con iNaturalist (avistamientos ciudadanos + fotos)
    path('inaturalist/', views.inaturalist_buscar, name='inaturalist_buscar'),

    path('panel/', views.panel_admin, name='panel_admin'),
    path('panel/usuario/<int:usuario_id>/rol/', views.cambiar_rol, name='cambiar_rol'),


]
