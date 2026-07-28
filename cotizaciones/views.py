import json
import urllib.parse
from io import BytesIO
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.template.loader import get_template
from django.conf import settings
from xhtml2pdf import pisa
from productos.models import Producto
from .models import Cotizacion, CotizacionItem
from .forms import CotizacionForm

def cotizar(request):
    form = CotizacionForm()
    return render(request, "cotizaciones/cotizar.html", {"form": form})

@require_POST
def crear_cotizacion(request):
    form = CotizacionForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    productos_data = request.POST.get("productos", "[]")
    try:
        productos_data = json.loads(productos_data)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Lista de productos inválida"}, status=400)

    if not productos_data:
        return JsonResponse({"error": "Debes seleccionar al menos un producto"}, status=400)

    cotizacion = Cotizacion.objects.create(
        usuario=request.user if request.user.is_authenticated else None,
        nombre=form.cleaned_data["nombre"],
        email=form.cleaned_data["email"],
        telefono=form.cleaned_data["telefono"],
        mensaje=form.cleaned_data["mensaje"],
    )

    total = 0
    for item_data in productos_data:
        producto = get_object_or_404(Producto, id=item_data["id"])
        cantidad = int(item_data.get("cantidad", 1))
        precio = float(producto.precio)
        total += cantidad * precio
        CotizacionItem.objects.create(
            cotizacion=cotizacion,
            producto=producto,
            producto_nombre=producto.nombre,
            cantidad=cantidad,
            precio_unitario=precio,
        )

    cotizacion.total = total
    cotizacion.save(update_fields=["total"])

    pdf_url = f"/cotizar/pdf/{cotizacion.id}/"
    host = request.get_host()
    scheme = request.scheme
    pdf_link = f"{scheme}://{host}{pdf_url}"

    whatsapp_url = ""
    if cotizacion.telefono:
        mensaje_wa = (
            f"Hola, soy {cotizacion.nombre}.\n"
            f"Mi cotización #{cotizacion.id} está lista:\n"
        )
        for item in cotizacion.items.all():
            mensaje_wa += f"• {item.producto_nombre} x{item.cantidad} = ${item.subtotal():.2f}\n"
        mensaje_wa += f"\n💰 Total: ${total:.2f}\n"
        mensaje_wa += f"\n📄 Descarga tu PDF aquí:\n{pdf_link}"
        whatsapp_url = f"https://wa.me/{cotizacion.telefono.replace('+', '').replace(' ', '')}?text={urllib.parse.quote(mensaje_wa)}"

    return JsonResponse({
        "ok": True,
        "cotizacion_id": cotizacion.id,
        "whatsapp_url": whatsapp_url,
        "email": cotizacion.email,
    })

def cotizacion_confirmada(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    return render(request, "cotizaciones/confirmada.html", {"cotizacion": cotizacion})

def cotizacion_pdf(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    template = get_template("cotizaciones/pdf_cotizacion.html")
    html = template.render({"cotizacion": cotizacion})
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if pdf.err:
        return HttpResponse("Error al generar PDF", status=500)
    response = HttpResponse(result.getvalue(), content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="cotizacion_{cotizacion.id}.pdf"'
    return response
