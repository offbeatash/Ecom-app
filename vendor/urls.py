from django.urls import path , include
from .views import *

urlpatterns = [
   
    path('ven_reg/',registaration_ven,name='ven_reg')

]  
