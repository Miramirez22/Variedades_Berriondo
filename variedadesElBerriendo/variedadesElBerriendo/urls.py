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

from general.views import index, search, product_detail, carrito, login_view, signup, profile, CustomLogoutView, profile_edit
# carrito, checkout
from general.views import add_to_cart, remove_from_cart, update_quantity, checkout, añadir_otro

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('carrito/', carrito, name='carrito'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('producto/<int:id>/', product_detail, name='product_detail'),
    path('carrito/', carrito, name='carrito'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:id>/', remove_from_cart, name='remove_from_cart'),
    path('update_quantity/<int:id>/', update_quantity, name='update_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('añadir_otro/<int:id>/', añadir_otro, name='añadir_otro'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
