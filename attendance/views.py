from django.shortcuts import render, redirect
from authapp.models import UserModel
from .models import AttendanceManagerModel, WOR_date, WeekAttendanceRoleManager
import datetime
import time
import json
from django.contrib.auth.decorators import login_required
@login_required(login_url='/login/')
# Create your views here.
def attendance(request):
    current_user_group = UserModel.objects.get(id=request.user.id).groups.first()
    current_week = datetime.datetime.now().isocalendar()[1]
    user_list = UserModel.objects.filter(groups=current_user_group)  

    # Filter the week_list queryset based on the current week and the next 11 weeks
    week_list = WOR_date.objects.filter(
        week_number__gt=current_week - 1,
        week_number__lt=current_week + 12
    )
    # Filter week roles by the current user's group and relevant weeks
    week_roles = WeekAttendanceRoleManager.objects.filter(
        users_group=current_user_group,
        week_id__week_number__gt=current_week - 1,
        week_id__week_number__lt=current_week + 12
    )
    # Filter AttendanceManagerModel queryset by users from the same group as the current user
    attendance_list = AttendanceManagerModel.objects.filter(
        person__groups=current_user_group,
        date__week_number__gt=current_week - 1,
        date__week_number__lt=current_week + 12
    ).select_related('person', 'date')    
    if request.POST.get('action') == 'update':
        week_no= int(request.POST.get('current_week'))
        user_status_dictionary = json.loads(request.POST.get('user_status_dictionary'))
        week_to_update = WOR_date.objects.get(week_number = week_no)
        for id in user_status_dictionary:
            try:
                person = UserModel.objects.get(id = id)
                new_attendance = AttendanceManagerModel.objects.get(date = week_to_update, person = person)
                if new_attendance.user_status == user_status_dictionary[id]:
                    continue
                else:     
                    new_attendance.user_status = user_status_dictionary[id]
                    new_attendance.save()
            except AttendanceManagerModel.DoesNotExist:
                new_attendance = AttendanceManagerModel.objects.create(
                    date = WOR_date.objects.get(week_number = week_no),
                    person = UserModel.objects.get(id = id),
                    user_status = user_status_dictionary[id],
                )
                new_attendance.save()
        return render(request, 'attendance-list.html', {
        'attendances': attendance_list, 
        'users': user_list, 
        'current_week': current_week, 
        'week_list' :  week_list,
        'week_roles' : week_roles
        })
    return render(request, 'attendance.html', {
        'attendances': attendance_list, 
        'users': user_list, 
        'current_week': current_week, 
        'week_list' :  week_list,
        'week_roles' : week_roles
        })

def attendance_history(request):
    current_user = UserModel.objects.get(id=request.user.id)
    user_list = UserModel.objects.filter(groups=current_user.groups.first())
    week_roles = WeekAttendanceRoleManager.objects.filter(users_group=current_user.groups.first()) 
    current_week = datetime.datetime.now().isocalendar()[1]

    attendance_list = AttendanceManagerModel.objects.all().select_related('person', 'date')

    week_list = WOR_date.objects.all()

    return render(request, 'attendance-history.html', {
        'attendances': attendance_list,
        'users': user_list,
        'current_week': current_week,
        'week_list': week_list,
        'week_roles': week_roles
    })