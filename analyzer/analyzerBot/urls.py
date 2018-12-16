from django.urls import path

from . import views

urlpatterns =[
    path('', views.index, name='index'),
    path('report/', views.generate_report, name='report'),
]