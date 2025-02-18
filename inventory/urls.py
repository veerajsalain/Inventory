from django.urls import path
from .views import add_stock, billing, low_stock_alert,  product_list, add_product, delete_product, sell_product, sales_history


urlpatterns = [
    path('', product_list, name='product_list'),
    path('add/', add_product, name='add_product'),
    path('delete/<int:product_id>/', delete_product, name='delete_product'),
    path('sell/<int:product_id>/', sell_product, name='sell_product'),
    path('sales/', sales_history, name='sales_history'),
    path('billing/<int:sale_id>/', billing, name='billing'),
    path('low-stock/', low_stock_alert, name='low_stock_alert'),
    path('add-stock/<int:product_id>/', add_stock, name='add_stock'),
]
