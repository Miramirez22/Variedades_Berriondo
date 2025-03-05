from django.contrib import admin
from .models import Producto, Categoria, Carrito, UserProfile  # Importa los modelos

# Registra los modelos en el panel de administración
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'stock', 'fecha_creacion')  # Muestra estas columnas
    list_filter = ('categoria',)  # Agrega filtros por categoría
    search_fields = ('nombre',)  # Agrega una barra de búsqueda por nombre

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Categoria)
admin.site.register(Carrito)
admin.site.register(UserProfile)
