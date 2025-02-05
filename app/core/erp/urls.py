from django.urls import path
from core.erp.views.category.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.area.views import *
from core.erp.views.domino.views import *
from core.erp.views.escala.views import *
from core.erp.views.pregunta.views import * 
from core.erp.views.votos.views import *
from core.erp.views.indicador.views import *
from core.erp.views.datos.views import *
from core.erp.views.datos1.views import *
from core.erp.views.limpiar.views import *


app_name = 'erp'

urlpatterns = [
    # home
    path('dashboard/', AllQuestionsListView.as_view(), name='dashboard'),
    # area
    path('area/list/', AreaListView.as_view(), name='area_list'),
    path('area/add/', AreaCreateView.as_view(), name='area_create'),
    path('area/update/<int:pk>/', AreaUpdateView.as_view(), name='area_update'),
    path('area/delete/<int:pk>/', AreaDeleteView.as_view(), name='area_delete'),
    # category
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # dominio
    path('dominio/list/', DominioListView.as_view(), name='dominio_list'),
    path('dominio/add/', DominioCreateView.as_view(), name='dominio_create'),
    path('dominio/update/<int:pk>/', DominioUpdateView.as_view(), name='dominio_update'),
    path('dominio/delete/<int:pk>/', DominioDeleteView.as_view(), name='dominio_delete'),
    # Escala
    path('escala/list/', EscalaListView.as_view(), name='escala_list'),
    path('escala/add/', EscalaCreateView.as_view(), name='escala_create'),
    path('escala/update/<int:pk>/', EscalaUpdateView.as_view(), name='escala_update'),
    path('escala/delete/<int:pk>/', EscalaDeleteView.as_view(), name='escala_delete'),
    # pregunta
    path('pregunta/list/', PreguntaListView.as_view(), name='pregunta_list'),
    path('pregunta/add/', PreguntaCreateView.as_view(), name='pregunta_create'),
    path('pregunta/update/<int:pk>/', PreguntaUpdateView.as_view(), name='pregunta_update'),
    path('pregunta/delete/<int:pk>/', PreguntaDeleteView.as_view(), name='pregunta_delete'),
    # votos
    path('votos/list/', VotosListView.as_view(), name='votos_list'),
    # indicador
    path('indicador/list/', IndicadorListView.as_view(), name='indicador_list'),
    path('indicador/add/', IndicadorCreateView.as_view(), name='indicador_create'),
    path('indicador/update/<int:pk>/', IndicadorUpdateView.as_view(), name='indicador_update'),
    path('indicador/delete/<int:pk>/', IndicadorDeleteView.as_view(), name='indicador_delete'),
    # autocompletado
    path('indicador-autocomplete/', IndicadorAutocomplete.as_view(), name='indicador_autocomplete'),
    #datos
    path('datos/list/', DatosListView.as_view(), name='datos_list'),
    path('datos/pdf/', DatosPDFView.as_view(), name='datos_pdf'),
    #datos 1
    path('datos_area/list/', DatosAreaListView.as_view(), name='datos_area_list'),
    path('datos_area/pdf/', DatosAreaPDFView.as_view(), name='datos_area_pdf'),
    #limpiar
    path('limpiar/list/', LimpiarDatosView.as_view(), name='limpiar_list'),
]   
