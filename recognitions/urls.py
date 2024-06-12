from django.urls import path

from .views import recognition_page, recognition_update

from src import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', recognition_page, name='recognition_page'),
    path('update/', recognition_update, name='recognition_update'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)