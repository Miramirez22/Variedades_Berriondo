from django.shortcuts import render, redirect, get_object_or_404
from general.models import Producto, Carrito
import random
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.

def index(request):
    # Obtener productos recomendados (6 aleatorios)
    productos_recomendados = list(Producto.objects.all())
    random.shuffle(productos_recomendados)
    productos_recomendados = productos_recomendados[:6]

    # Obtener productos por categoría (4 por cada una)
    ropa_y_zapatos = Producto.objects.filter(categoria__nombre="ropa")[:4]
    tecnologia = Producto.objects.filter(categoria__nombre="tecnologia")[:4]

    # Seleccionar 4 productos al azar para "Varios"
    todos_los_productos = list(Producto.objects.all())
    random.shuffle(todos_los_productos)
    varios = todos_los_productos[:4]

    return render(request, 'index.html', {
        'productos_recomendados': productos_recomendados,
        'ropa_y_zapatos': ropa_y_zapatos,
        'tecnologia': tecnologia,
        'varios': varios
    })

def search(request):
    query = request.GET.get('q', '')  # Obtiene la búsqueda
    categoria = request.GET.get('categoria', '')  # Obtiene la categoría
    precio_min = request.GET.get('precio_min', '')
    precio_max = request.GET.get('precio_max', '')

    productos = Producto.objects.all()

    if query:
        productos = productos.filter(nombre__icontains=query)  # Filtra por nombre

    if categoria:
        productos = productos.filter(categoria__nombre=categoria)  # Filtra por categoría

    if precio_min:
        productos = productos.filter(precio__gte=precio_min)  # Precio mínimo

    if precio_max:
        productos = productos.filter(precio__lte=precio_max)  # Precio máximo

    return render(request, 'search.html', {'productos': productos})

def product_detail(request, id):
    # Obtener producto por ID
    producto = get_object_or_404(Producto, id=id)

    # Obtener productos similares (de la misma categoría, excluyendo el actual)
    productos_similares = Producto.objects.filter(categoria=producto.categoria).exclude(id=producto.id)[:3]
    
    # si hay menos de 3 productos similares, agregar productos aleatorios
    if productos_similares.count() < 3:
        productos_random = Producto.objects.exclude(id=producto.id).order_by('?')[:(3 - productos_similares.count())]
        productos_similares = productos_similares | productos_random
    productos_similares = productos_similares[:3]

    return render(request, 'product_detail.html', {
        'producto':producto, 
        'productos_similares': productos_similares })

# Decorador para requerir login
@login_required(login_url='login')
def carrito(request):
    # Obtener carrito del usuario
    carrito_items = Carrito.objects.filter(usuario=request.user)
    # calcular el precio total
    total_price = sum([item.producto.precio * item.cantidad for item in carrito_items])

    # adaptar cantidad de producto
    if request.method == 'POST':
        for item in carrito_items:
            cantidad = request.POST.get(f'cantidad_{item.id}')
            if cantidad:
                try:
                    cantidad = int(cantidad)
                    if cantidad > 0:
                        item.cantidad = cantidad
                        item.save()
                except ValueError:
                    pass  # número invalido
        return redirect('carrito')
    
    return render(request, 'carrito.html', {
        'carrito': carrito,
        'carrito_items': carrito_items,
        'total_price': total_price
    })


@login_required(login_url='login')
def add_to_cart(request, id):
    producto = get_object_or_404(Producto, id=id)

    carrito_item, created = Carrito.objects.get_or_create(
        usuario=request.user,
        producto=producto,
        )
    
    if not created:
        carrito_item.cantidad += 1
        carrito_item.save()

    return redirect('carrito')

def remove_from_cart(request, id):
    carrito_item = get_object_or_404(Carrito, id=id)
    carrito_item.delete()
    return redirect('carrito')

@login_required
def update_quantity(request, id):
    try:
        item = Carrito.objects.get(id=id, usuario=request.user)
        cantidad = request.POST.get(f'cantidad_{item.id}')
        if cantidad:
            try:
                cantidad = int(cantidad)
                if cantidad > 0:
                    item.cantidad = cantidad
                    item.save()
            except ValueError:
                pass  
    except Carrito.DoesNotExist:
        pass
    return redirect('carrito')

def checkout(request):
    total_price = sum(item.subtotal for item in request.user.carrito_set.all())

    context = {
        'total_price': total_price
    }

    return render(request, 'checkout.html', context)

def añadir_otro(request, id):
    item = get_object_or_404(Carrito, id=id, usuario=request.user)
    item.cantidad += 1
    item.save()
    return redirect('checkout')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Inicia sesión automáticamente
            return redirect("profile")  # Redirige al perfil
    else:
        form = CustomUserForm()
    return render(request, "signup.html", {"form": form})

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html', {'profile': request.user})


from django.contrib.auth.views import LogoutView
class CustomLogoutView(LogoutView):
    next_page = 'index'

