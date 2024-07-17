"""
URL configuration for IMS project.

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
from stocks.views import *

urlpatterns = [
    
    path('products/create/', Product_createView.as_view(), name='product-create'),#for creating new products

    path('products/', Product_listView.as_view(), name='product-list'),#for viewing the entire products

    path('add-products/',Add_stock_view.as_view()),#for adding specific product variant,if it exist increase its quantity

    path('products/remove-stock/', Remove_stock_view.as_view(), name='remove-stock'),#for removing a specific product variant.
]
