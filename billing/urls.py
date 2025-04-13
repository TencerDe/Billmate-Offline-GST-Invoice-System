from django.urls import path
from . import views

urlpatterns = [
    path('add-customer/', views.add_customer),
    path('delete-customer/<int:customer_id>/', views.delete_customer),

    path('add-product/', views.add_product),
    path('delete-product/<int:product_id>/', views.delete_product),

    path('create-invoice/', views.create_invoice),

    path("customers/", views.get_customer, name="get_customers"),
    path("products/", views.get_products, name="get_products"),

]
