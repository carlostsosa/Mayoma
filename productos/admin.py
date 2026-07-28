from django.contrib import admin
from .models import Categoria, Producto

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "orden", "created_at"]
    prepopulated_fields = {"slug": ("nombre",)}

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "categoria", "precio", "stock", "destacado", "created_at"]
    list_filter = ["categoria", "stock", "destacado"]
    search_fields = ["nombre", "descripcion"]
    prepopulated_fields = {"slug": ("nombre",)}
    list_editable = ["precio", "stock", "destacado"]
