from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order/', views.OrderView.as_view(), name='order_item'),
    path('create/order/', views.create_order, name='create_order'),
    path('cart/', views.OrderSummaryView.as_view(), name='summary_cart'),
    # this under usl`s for add and remove and delete product from order
    path('add/<slug:product_slug>/', views.add_to_cart, name='add_cart'),
    path('remove/cart/<slug:product_slug>/', views.remove_from_cart, name='remove_cart'),
    path('remove/one/<slug:product_slug>/', views.remove_one_cart, name='remove_one_cart'),
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
    path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),

]
