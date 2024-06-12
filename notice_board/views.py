from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
@login_required
def notice_board(request):
    return render(request, 'power-bi.html', {
          'firstname' : request.user.first_name,
          'lastname' : request.user.last_name,
     })