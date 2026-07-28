from django.shortcuts import render, get_object_or_404
from .models import Producto, Categoria

def catalogo(request):
    categoria_slug = request.GET.get("categoria")
    query = request.GET.get("q")
    productos = Producto.objects.filter(stock=True)
    categorias = Categoria.objects.all()

    if categoria_slug:
        productos = productos.filter(categoria__slug=categoria_slug)
    if query:
        productos = productos.filter(nombre__icontains=query)

    context = {
        "productos": productos,
        "categorias": categorias,
        "categoria_activa": categoria_slug,
    }
    return render(request, "productos/catalogo.html", context)

def detalle_producto(request, slug):
    producto = get_object_or_404(Producto, slug=slug, stock=True)
    return render(request, "productos/detalle.html", {"producto": producto})
