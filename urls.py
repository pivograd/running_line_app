from django.urls import path
from . import views

app_name = 'running_line'

urlpatterns = [
    path('generate/<str:text>', views.generate_running_line, name='generate_running_line'),
    path('generate/', views.generate, name='generate_page'),
    path('', views.view_for_redirect),
]



