from django.urls import path
from .views import *

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('category/<slug>', CategoryView.as_view(), name='category'),
    path('subcategory/<slug>', SubCategoryView.as_view(), name='subcategory'),

    

]
