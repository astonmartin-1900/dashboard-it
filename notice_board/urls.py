from django.urls import path
from notice_board.views import notice_board


urlpatterns = [
    path('', notice_board, name='notice_board'),
]

