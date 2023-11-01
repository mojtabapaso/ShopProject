from django.urls import path

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('brand/<slug:brand_slug>/', views.HomeView.as_view(), name='brand_slug'),
    path('category/<slug:slug_category>', views.HomeView.as_view(), name='category_slug'),
    # show product in pages
    path('<slug:slug>/', views.ProductsDetailView.as_view(), name='product_detail'),

    # Commend
    path('reply/<int:product_id>/<int:commend_id>/', views.AddCommendView.as_view(), name='add_reply'),
]

