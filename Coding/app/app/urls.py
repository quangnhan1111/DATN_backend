"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('brands.urls')),
    path('api/v1/', include('categories.urls')),
    path('api/v1/', include('subcategories.urls')),
    path('api/v1/', include('posts.urls')),
    path('api/v1/', include('coupons.urls')),
    path('api/v1/', include('chats.urls')),
    path('api/v1/', include('reviews.urls')),
    path('api/v1/', include('customers.urls')),
    path('api/v1/', include('staffs.urls')),
    path('api/v1/', include('roles.urls')),
    path('api/v1/', include('sales.urls')),
    path('api/v1/', include('notifications.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('invoices.urls')),
    path('api/v1/', include('colors.urls')),
]
