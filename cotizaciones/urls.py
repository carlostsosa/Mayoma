from django.urls import path
from . import views

app_name = "cotizaciones"

urlpatterns = [
    path("", views.cotizar, name="cotizar"),
    path("crear/", views.crear_cotizacion, name="crear"),
    path("confirmada/<int:cotizacion_id>/", views.cotizacion_confirmada, name="confirmada"),
    path("pdf/<int:cotizacion_id>/", views.cotizacion_pdf, name="pdf"),
]
