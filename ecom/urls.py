from django.urls import path
from .views import *

urlpatterns = [
    path('demo/', demo, name='demo'),
    path('first/', first, name='first'),
    path('style/', style, name='style'),
    path('show/', show, name='show'),
    path('showimg/', showimg, name='showimg'),
    path('store/', store, name='store'),
    #path('storeget/', storeget, name='storeget'),
    path('storeimg/', storeimg, name='storeimg'),
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('product/<int:id>', product, name='product'),
    path('product_detail/<int:id>', product_detail, name='product_detail'),
    path('profile/', profile, name='profile')

] 
