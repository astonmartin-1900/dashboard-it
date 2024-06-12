from django.urls import path
from attendance.views import attendance, attendance_history


urlpatterns = [
    path('', attendance, name='attendance_page'),
    path('history/', attendance_history, name='attendance_history'),
]

