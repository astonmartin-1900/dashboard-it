from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # new



from django.conf import settings

from django.views.static import serve

urlpatterns = [
    path('', include('authapp.urls', namespace='authapp')),
    path('admin/', admin.site.urls),
    path('actions/', include(('actions.urls', 'actions'), namespace='actions')),
    path('attendance/', include(('attendance.urls', 'recognition_page'), namespace='attendance')),
    path('improvements/', include(('improvements.urls', 'improvements'), namespace='improvements')),
    path('notice-board/', include(('notice_board.urls', 'notice_board'), namespace='notice-board')),
    path('recognitions/', include(('recognitions.urls', 'recognition_page'), namespace='recognitions')),
    path('she/', include(('she.urls', 'she_page'), namespace='she')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
