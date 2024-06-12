from django.conf.urls.static import static
from src import settings
from django.urls import path, include
from .views import actions, actions_history

urlpatterns = [
    path('', actions, name='action_main'),
    path('history/', actions_history, name='actions_history'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
