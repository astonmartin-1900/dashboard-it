from django.urls import path
from .views import improvements, improvement_edit, change_status

urlpatterns = [
    path('', improvements, name='improvements_main'),
    path('edit/<int:pk>', improvement_edit, name='improvement_edit'),
    path('status/<int:pk>', change_status, name='change_status'),
]