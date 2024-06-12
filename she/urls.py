from django.urls import path
from she.views import she_main


urlpatterns = [
    path('', she_main, name='she_main'),
]

