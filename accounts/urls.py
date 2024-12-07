from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
app_name = 'accounts'
urlpatterns = [
    path('register/', views.register_form, name="register"), #registers  urls
    path('login/', views.login_view, name="login"), #Login url
    # Logout URL
    path('logout/', views.logout_view, name='logout'),

]
