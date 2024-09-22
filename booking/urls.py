from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('device-calendar/<device_id>', views.device_calendar, name='device_calendar'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('api/bookings/<device_id>', views.api_bookings, name='api_bookings'),
    path('api/get-one-booking/<booking_id>', views.api_get_one_booking, name='get_one_booking'),
    path('api/get-username/<user_id>', views.api_get_username, name='get_username'),
    path('api/addbooking/', views.add_booking, name='add_booking'),
    path('api/editbooking/<booking_id>', views.edit_booking, name='edit_booking'),
    path('api/delete/<booking_id>', views.delete_booking, name='delete_booking'),
]
