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

from general.views import index, search, product_detail, carrito, login_view, signup, profile, CustomLogoutView, add_to_cart


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('profile/', profile, name='profile'),
    path('carrito/', carrito, name='carrito'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('', index, name='index'),
    path('search/', search, name='search'),
    path('producto/<int:id>/', product_detail, name='product_detail'),
    path('carrito/', carrito, name='carrito'),
    path('add_to_cart/<int:id>/', add_to_cart, name='add_to_cart'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
