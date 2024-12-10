from django.urls import path
from . import views
app_name = 'perl_app'
urlpatterns = [
    # Resort management URLs
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('client_dashboard/', views.client_dashboard, name= 'client_dashboard'),
    path('services/', views.services, name = 'services'),
    path('resort/', views.resort_list, name='resort_list'),
    path('resort/create/', views.add_edit_resort, name='resort_create'),  # For creating new resorts
    path('resort/edit/<int:pk>/', views.ResortEditView.as_view(), name='resort_edit'),  # Use as_view() to call the class-based view
    path('resort/delete/<int:pk>/', views.ResortDeleteView.as_view(), name='resort_delete'),

    # Booking management URLs
    path('bookings/', views.booking_list, name='booking_list'),
    path('booking/create/', views.book_resort, name='book_resort'),
     path('resort/<int:pk>/book/', views.confirm_booking, name='confirm_booking'),
    path('booking/confirmation/<int:pk>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/approve/<int:pk>/', views.approve_booking, name='approve_booking'), 
    path('booking/cancel/<int:pk>/', views.booking_cancel, name='booking_cancel'),

    # Settings URL
    path('settings/', views.settings, name='settings'),

 
   

    
]
