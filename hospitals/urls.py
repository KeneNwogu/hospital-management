from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('hospitals/', views.all_hospitals, name='hospitals'),
    path('hospital/<str:hospital_id>/', views.get_detail, name='get_detail'),
]
