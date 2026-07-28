from django.shortcuts import render
from productos.models import Producto, Categoria

def home(request):
    destacados = Producto.objects.filter(destacado=True, stock=True)[:8]
    categorias = Categoria.objects.all()
    return render(request, "pages/home.html", {
        "destacados": destacados,
        "categorias": categorias,
    })

def quienes_somos(request):
    return render(request, "pages/quienes_somos.html")
