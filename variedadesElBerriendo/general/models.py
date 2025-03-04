from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name="productos")
    imagen = models.ImageField(upload_to="productos/", blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=now)

    def __str__(self):
        return self.nombre

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Carrito de {self.usuario.username}"

    @property
    def subtotal(self):
        return self.producto.precio * self.cantidad

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiration_date = models.DateField(blank=True, null=True)
    cvv = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        return self.user.username
