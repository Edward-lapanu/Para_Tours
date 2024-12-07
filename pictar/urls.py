from django.urls import path
from . import views
app_name= 'pictar'
urlpatterns = [
     path('guides/', views.guides_list, name="guides"),
]