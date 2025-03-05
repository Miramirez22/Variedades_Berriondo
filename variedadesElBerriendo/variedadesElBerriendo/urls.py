"""
URL configuration for variedadesElBerriendo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from general.views import (
    index, search, product_detail, carrito, login_view, signup, profile, profile_edit,
    address_add, address_delete, address_prefer, payment_method_add, payment_method_delete, payment_method_prefer, CustomLogoutView, add_to_cart, remove_from_cart, update_quantity, checkout, añadir_otro,
    #ccmm
    admin_panel,admin_productos,admin_usuarios,admin_ordenes,agregar_producto,editar_producto, eliminar_producto,
    agregar_usuario, editar_usuario, eliminar_usuario, editar_orden
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('address/add/', address_add, name='address_add'),
    path('address/delete/<int:id>/', address_delete, name='address_delete'),
    path('address/prefer/<int:id>/', address_prefer, name='address_prefer'),
    path('payment_method/add/', payment_method_add, name='payment_method_add'),
    path('payment_method/delete/<int:id>/', payment_method_delete, name='payment_method_delete'),
    path('payment_method/prefer/<int:id>/', payment_method_prefer, name='payment_method_prefer'),
    path('carrito/', carrito, name='carrito'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('producto/<int:id>/', product_detail, name='product_detail'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('update_quantity/<int:id>/', update_quantity, name='update_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('añadir_otro/<int:id>/', añadir_otro, name='añadir_otro'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'), name='password_change_done'),

    #panel de administrador
    path('admin_panel/', admin_panel, name='admin_panel'),

    #panel de administrar productos
    path('admin_panel/admin_productos/', admin_productos, name='admin_productos'),
    path('admin_panel/admin_productos/agregar_producto/', agregar_producto, name='agregar_producto'),
    path('admin_panel/admin_productos/editar/<int:id>/', editar_producto, name='editar_producto'),
    path('admin_panel/admin_productos/eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),
    #panel de administrar usuarios
    path('admin_usuarios/', admin_usuarios, name='admin_usuarios'),

    path('admin_usuarios/agregar_usuario/', agregar_usuario, name='agregar_usuario'),
    path('admin_usuarios/editar_usuario/<int:usuario_id>/', editar_usuario, name='editar_usuario'),
    path('admin_usuarios/eliminar_usuario/<int:usuario_id>/', eliminar_usuario, name='eliminar_usuario'),

    # Panel de administrar ordenes
    path('admin_panel/admin_ordenes/', admin_ordenes, name='admin_ordenes'),
    
    path('editar_orden/<int:order_id>/', editar_orden, name='editar_orden'),  

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)