from django.db import models
from django.conf import settings

class Cotizacion(models.Model):
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("enviada", "Enviada"),
        ("respondida", "Respondida"),
    ]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=200, verbose_name="Nombre completo")
    email = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, verbose_name="Teléfono")
    mensaje = models.TextField(blank=True, verbose_name="Comentarios")
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Cotización #{self.id} - {self.nombre}"

    def calcular_total(self):
        self.total = sum(item.subtotal() for item in self.items.all())
        self.save(update_fields=["total"])

class CotizacionItem(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="items")
    producto = models.ForeignKey("productos.Producto", on_delete=models.SET_NULL, null=True)
    producto_nombre = models.CharField(max_length=200)
    cantidad = models.PositiveIntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Item de cotización"
        verbose_name_plural = "Items de cotización"

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad}x {self.producto_nombre}"
