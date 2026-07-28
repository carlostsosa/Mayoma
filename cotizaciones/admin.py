from django.contrib import admin
from .models import Cotizacion, CotizacionItem

class CotizacionItemInline(admin.TabularInline):
    model = CotizacionItem
    readonly_fields = ["producto_nombre", "cantidad", "precio_unitario"]
    can_delete = False
    extra = 0

@admin.register(Cotizacion)
class CotizacionAdmin(admin.ModelAdmin):
    list_display = ["id", "nombre", "email", "total", "estado", "created_at"]
    list_filter = ["estado"]
    search_fields = ["nombre", "email"]
    inlines = [CotizacionItemInline]
    readonly_fields = ["total"]
