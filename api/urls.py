from django.urls import path
from . import views

urlpatterns = [
    path('',views.getData),
    path('country_info/<str:city>/',views.home),
]
