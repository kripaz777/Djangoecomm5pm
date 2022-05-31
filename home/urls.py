from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', CategoryView.as_view(), name='category'),
    path('subcategory/<slug>', SubCategoryView.as_view(), name='subcategory'),
    path('search', SearchView.as_view(), name='search'),
    path('details/<slug>', ProductDetailView.as_view(), name='details'),
    path('signup', signup, name='signup'),
    path('cart/<slug>', cart, name='cart'),
    path('mycart', CartView.as_view(), name='mycart'),
    path('delete_mycart/<slug>', delete_cart, name='delete_mycart'),    
    path('reduce_mycart/<slug>', reduce_cart_quantity, name='reduce_mycart'),



]
