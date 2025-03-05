from django.shortcuts import render, redirect, get_object_or_404
from general.models import Producto, Carrito
import random
from django.contrib.auth.decorators import login_required
from .forms import CustomUserForm, PaymentForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .models import UserProfile
from django.contrib.auth import update_session_auth_hash
from .forms import UserForm, UserProfileForm, AddressForm, PaymentMethodForm, PasswordChangeForm
from .models import UserProfile, Address, PaymentMethod, Order
from django.contrib.auth.views import LogoutView


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
    form = PaymentForm()
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            # Procesar pago
            return redirect('index')
    else:
        form = PaymentForm()
    
    context = {
        'total_price': total_price,
        'form': form
    }

    return render(request, 'checkout.html', context)

def añadir_otro(request, id):
    item = get_object_or_404(Carrito, id=id, usuario=request.user)
    item.cantidad += 1
    item.save()
    return redirect('checkout')



def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("profile")
        else:
            return render(request, "login.html", {"error": "Nombre de usuario o contraseña incorrectos"})
        
    if request.user.is_authenticated:
        return redirect("profile")
    
    return render(request, "login.html")

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
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    addresses = Address.objects.filter(user=request.user)
    payment_methods = PaymentMethod.objects.filter(user=request.user)
    orders = Order.objects.filter(user=request.user)

    context = {
        'user_profile': user_profile,
        'addresses': addresses,
        'payment_methods': payment_methods,
        'orders': orders,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def profile_edit(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, instance=user_profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    return render(request, 'profile_edit.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required(login_url='login')
def address_add(request):
    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('profile')
    else:
        form = AddressForm()
    return render(request, 'address_form.html', {'form': form})

@login_required(login_url='login')
def address_delete(request, id):
    address = get_object_or_404(Address, id=id, user=request.user)
    address.delete()
    return redirect('profile')

@login_required(login_url='login')
def address_prefer(request, id):
    Address.objects.filter(user=request.user).update(is_preferred=False)
    address = get_object_or_404(Address, id=id, user=request.user)
    address.is_preferred = True
    address.save()
    return redirect('profile')

@login_required(login_url='login')
def payment_method_add(request):
    if request.method == "POST":
        form = PaymentMethodForm(request.POST)
        if form.is_valid():
            payment_method = form.save(commit=False)
            payment_method.user = request.user
            payment_method.save()
            return redirect('profile')
    else:
        form = PaymentMethodForm()
    return render(request, 'payment_method_form.html', {'form': form})

@login_required(login_url='login')
def payment_method_delete(request, id):
    payment_method = get_object_or_404(PaymentMethod, id=id, user=request.user)
    payment_method.delete()
    return redirect('profile')

@login_required(login_url='login')
def payment_method_prefer(request, id):
    PaymentMethod.objects.filter(user=request.user).update(is_preferred=False)
    payment_method = get_object_or_404(PaymentMethod, id=id, user=request.user)
    payment_method.is_preferred = True
    payment_method.save()
    return redirect('profile')

@login_required(login_url='login')
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']
            if new_password == confirm_password:
                user = request.user
                if user.check_password(old_password):
                    user.set_password(new_password)
                    user.save()
                    update_session_auth_hash(request, user)  # Mantiene la sesión después de cambiar la contraseña
                    return redirect('profile')
                else:
                    form.add_error('old_password', 'Contraseña actual incorrecta')
            else:
                form.add_error('confirm_password', 'Las contraseñas no coinciden')
    else:
        form = PasswordChangeForm()
    return render(request, 'change_password.html', {'form': form})

#panel de admin
@login_required
def admin_panel(request):
    total_productos = Producto.objects.count()  # total de productos
    total_usuarios = UserProfile.objects.count()  # Total de usuarios registrados
    total_ordenes = Order.objects.count() #total de orenes 
    return render(request, 'admin_panel/admin_panel.html', {'total_productos': total_productos,'total_usuarios': total_usuarios, 'total_ordenes':total_ordenes})

#productos en admin_panel
def admin_productos(request):
    total_productos = Producto.objects.count()
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'admin_panel/admin_productos.html', {'total_productos': total_productos, 'productos': productos})

#seccion de pag de productos
from .forms import ProductoForm, UserForm
 
def agregar_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_productos')
    else:
        form = ProductoForm()

    return render(request, 'admin_panel/admin_prod/agregar_producto.html', {'form': form})

def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)  # Busca el producto

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('admin_productos') 
        else:
            print("Errores del formulario:", form.errors)  # depura errores
    else:
        form = ProductoForm(instance=producto)  # Cargar producto en el formulario

    return render(request, 'admin_panel/admin_prod/editar_producto.html', {'form': form})


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect

@csrf_exempt  # Solo si no pasas CSRF en el request, pero mejor usa el token
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == "POST":
        producto.delete()
        return JsonResponse({"success": True})  # Devuelve JSON en vez de redirigir

    return JsonResponse({"error": "Método no permitido"}, status=400)


#usuarios en admin_panel
def admin_usuarios(request):
    total_usuarios = UserProfile.objects.count()
    usuarios = UserProfile.objects.all()  # Obtener todos los usuarios
    return render(request, 'admin_panel/admin_usuarios.html', {'total_usuarios': total_usuarios, 'usuarios': usuarios})

def admin_usuarios(request):
    usuarios = UserProfile.objects.all()
    return render(request, 'admin_panel/admin_usuarios.html', {'usuarios': usuarios})

def agregar_usuario(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_usuarios')
    else:
        form = UserForm()

    return render(request, 'admin_panel/agregar_usuario.html', {'form': form})

def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(UserForm, id=usuario_id)
    if request.method == "POST":
        form = UserForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('admin_usuarios')
    else:
        form = UserForm(instance=usuario)

    return render(request, 'admin_panel/editar_usuario.html', {'form': form, 'usuario': usuario})

def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(UserProfile, id=usuario_id)
    if request.method == "POST":
        usuario.delete()
        return redirect('admin_usuarios')

    return render(request, 'admin_panel/eliminar_usuario.html', {'usuario': usuario})




#Ordenes en admin_panel
def admin_ordenes(request):
    total_ordenes = Order.objects.count()
    ordenes = Order.objects.all()  # Obtener todas las órdenes
    return render(request, 'admin_panel/admin_ordenes.html', {'total_ordenes': total_ordenes, 'ordenes': ordenes})



class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)  # Forzar que GET funcione como POST

