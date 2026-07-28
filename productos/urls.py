from django.urls import path
from . import views

app_name = "productos"

urlpatterns = [
    path("", views.catalogo, name="catalogo"),
    path("<slug:slug>/", views.detalle_producto, name="detalle"),
]
