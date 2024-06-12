from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .forms import UserRegistration, UserEditForm
from .models import UserModel, GroupAdmin
from recognitions.models import RecognitionManagerModel
from attendance.models import AttendanceManagerModel, WOR_date, WeekAttendanceRoleManager
from actions.models import ActionTaskManagerModel
import datetime
from datetime import timedelta
import time
from django.core.cache import cache

# Create your views here.
def user_present(user_id):
    date = datetime.datetime.now()
    user_last_login = UserModel.objects.get(pk = user_id).last_login + timedelta(hours = 2)
    user_last_login_date = user_last_login.strftime('%y-%m-%d')
    user_last_login_time = user_last_login.strftime('%H')
    current_date = date.strftime('%y-%m-%d')
    current_time = date.strftime('%H')

    if (user_last_login_date == current_date and int(current_time)- int(user_last_login_time) <2):
        return True
    else:
        return False
@login_required(login_url='/login/')   
def wor_dates_generator(request):
    today = datetime.datetime.today()
    date = today
    # Generating Weeks
    for i in range(52):
        current_week = date.strftime("%V")
        # Calculate the date for the Monday of the current week
        monday = date - timedelta(days=date.weekday())
        # Calculate the date for the Sunday of the current week
        sunday = monday + timedelta(days=6)

        if current_week[0] == "0":
            current_week = int(current_week) % 10
        else:
            current_week = current_week 
        WOR_date.objects.get_or_create(
            start_date = monday,
            end_date = sunday,
            week_number = current_week,
        )
        date = date + datetime.timedelta(days=7)
    return redirect('/accounts/settings/')

@login_required(login_url='/login/')
def dashboard(request):
    profile_information = UserModel.objects.get(id=request.user.pk)
    recognition = RecognitionManagerModel.objects.get(user_profile = request.user)
    actions_list = ActionTaskManagerModel.objects.filter(
        action_group =  UserModel.objects.get(id = request.user.id).groups.first(),
        assigned_user = profile_information,
        action_status = "draft" 
    )
    users_list =  UserModel.objects.filter(groups =  UserModel.objects.get(id = request.user.id).groups.first())
    return render(request, 'authapp/dashboard.html', { 
        'profile_information': profile_information,
        'recognitions': recognition, 
        'actions': actions_list,
        'users': users_list,
        })
@login_required(login_url='/login/')
def agenda(request):
    user = UserModel.objects.get(id=request.user.id)
    group = user.groups.first()
    current_week = datetime.datetime.now().strftime("%V")
    week_roles = WeekAttendanceRoleManager.objects.select_related('users_group', 'week_id').filter(
        users_group=group,
        week_id__week_number=current_week
    )
    current_week_roles = WeekAttendanceRoleManager.objects.filter(
        users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
        week_id = WOR_date.objects.get(week_number = current_week)
    )

    try:
        this_group_admin = GroupAdmin.objects.get(group=group).admin
    except GroupAdmin.DoesNotExist:
        this_group_admin = ""

    next_week_number = str(int(current_week) + 1)
    next_week_roles = WeekAttendanceRoleManager.objects.select_related('users_group', 'week_id').filter(
        users_group=group,
        week_id__week_number=next_week_number
    )

    message = ""
    if request.POST.get('action') == 'change_leader':
        if user_present(week_roles.wor_leader.pk):
            message = "wor_leader"
        elif user_present(week_roles.wor_engager.pk) and request.user == week_roles.wor_engager:
            next_week_roles.wor_leader = week_roles.wor_leader
            next_week_roles.save()
            week_roles.wor_leader = week_roles.wor_engager
            week_roles.save()
            message = "wor_engager"
        else:
            this_week_leader = week_roles.wor_leader
            week_roles.wor_leader = request.user
            week_roles_list = WeekAttendanceRoleManager.objects.filter(users_group=group).filter(
                week_id__week_number__gt=current_week, wor_leader=request.user
            )
            for week in week_roles_list:
                week.wor_leader = this_week_leader
                week.save()
                break
            week_roles.save()

        try:
            wor_leader_present = user_present(current_week_roles[0].wor_leader.pk)
            wor_engager_present = user_present(current_week_roles[0].wor_engager.pk)
        except:
            wor_leader_present = False
            wor_engager_present = False
    
        context = {
            "wor_leader_present": wor_leader_present,
            "wor_engager_present": wor_engager_present,
            "message": message,
            "week_role": week_roles,
            "current_week_roles": current_week_roles,
            "next_week_role": next_week_roles
        }
        return render(request, 'account/agenda-facilitators.html', context=context)
    
    try:
        wor_leader_present = user_present(current_week_roles[0].wor_leader.pk)
        wor_engager_present = user_present(current_week_roles[0].wor_engager.pk)
    except:
        wor_leader_present = False
        wor_engager_present = False

    context = {
        "wor_leader_present": wor_leader_present,
        "wor_engager_present": wor_engager_present,
        "message": message,
        "week_roles": week_roles,
        "current_week_roles": current_week_roles,
        "next_week_roles": next_week_roles,
    }
    return render(request, 'account/agenda.html', context=context)

@login_required(login_url='/login/')
def wor_calendar_generation(request):
    current_user = UserModel.objects.get(id=request.user.id)
    user_group = current_user.groups.first()
    current_group_user_list = UserModel.objects.filter(groups=user_group)
    print(current_group_user_list)
    ready_selected = current_group_user_list[0].id

    # Collect updates in a list
    updates = []

    for week in WOR_date.objects.all():
        for j in range(current_group_user_list.count()):
            if current_group_user_list[j].id == ready_selected:
                week_id=WOR_date.objects.get(week_number=week.week_number)
                if current_group_user_list[j] == current_group_user_list[current_group_user_list.count() - 1]:
                    print("List breaks on "+ str(current_group_user_list[j]))
                    try:
                        WeekAttendanceRole = WeekAttendanceRoleManager.objects.get(
                            week_id=week_id,
                            users_group=user_group
                        )
                        WeekAttendanceRole.wor_leader = current_group_user_list[j]
                        WeekAttendanceRole.wor_engager = current_group_user_list[0]
                        updates.append(WeekAttendanceRole)
                        ready_selected = current_group_user_list[0].id
                        break
                    except WeekAttendanceRoleManager.DoesNotExist:
                        WeekAttendanceRole = WeekAttendanceRoleManager(
                            week_id=week_id,
                            users_group=user_group,
                            wor_leader=current_group_user_list[j],
                            wor_engager=current_group_user_list[0],
                        )
                        updates.append(WeekAttendanceRole)
                        ready_selected = current_group_user_list[0].id
                        break
                else:
                    print("List continue with user "+ str(current_group_user_list[j]))
                    try:
                        WeekAttendanceRole = WeekAttendanceRoleManager.objects.get(
                            week_id=week_id,
                            users_group=user_group
                        )
                        WeekAttendanceRole.wor_leader = current_group_user_list[j]
                        WeekAttendanceRole.wor_engager = current_group_user_list[j + 1]
                        print("WeekAttendanceRole.wor_engager"+ str(ready_selected))
                        updates.append(WeekAttendanceRole)
                        ready_selected = current_group_user_list[j + 1].id

                        break
                    except WeekAttendanceRoleManager.DoesNotExist:
                        WeekAttendanceRole = WeekAttendanceRoleManager(
                            week_id=week_id,
                            users_group=user_group,
                            wor_leader=current_group_user_list[j],
                            wor_engager=current_group_user_list[j + 1],
                        )
                        updates.append(WeekAttendanceRole)
                        ready_selected = current_group_user_list[j + 1].id
                        break

    # Bulk update the changes
    for update in updates:
        update.save()

    return redirect('/accounts/settings/')

@login_required(login_url='/login/')
def register(request):
    if request.method == 'POST':
        form = UserRegistration(request.POST, request.FILES)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(
                form.cleaned_data.get('password')
            )
            new_user.save()
            time.sleep(1)

            new_user.groups.add(UserModel.objects.get(id = request.user.id).groups.first())
            new_user.last_login = datetime.datetime.now() - timedelta(hours = 8)
            new_user.save()

            RecognitionManagerModel.objects.get_or_create(
                user_profile = UserModel.objects.get(id = new_user.id)
            )
            time.sleep(1)
            # Need to add the calendar update
            user_calendar_update(request)
            # Finishing of calendar update code
            return redirect("/accounts/settings/")
    else:
        form = UserRegistration()
    context = {
        "form": form
    }

    return render(request, 'authapp/register.html', context=context)

@login_required(login_url='/login/')
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, request.FILES, instance=request.user,)
        if user_form.is_valid():
            user = UserModel.objects.get(id = request.user.id)
            user.user_image.delete()
            user_form.save()
            return redirect("/accounts/profile/")
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'form': user_form,
    }
    return render(request, 'authapp/edit.html', context=context)

@login_required(login_url='/login/')
def settings(request):
    if request.POST.get('operation') == 'generate-remove-user-list':
        try:
            user_list = UserModel.objects.filter(groups = UserModel.objects.get(id = request.user.id).groups.first())            
            return render(request, 'account/actions/user-to-remove.html', {
                'users': user_list, 
            })
        except:
            return render(request, 'account/actions/user-to-remove.html', {
                'users': user_list, 
            })
    elif request.POST.get('operation') == 'generate-add-user-list':
        try:
            unassigned_users_list = UserModel.objects.filter(groups = None)           
            return render(request, 'account/actions/user-to-add.html', {
                'unassigned_users_list': unassigned_users_list, 
            })
        except:
            return render(request, 'account/actions/user-to-add.html', {
                'unassigned_users_list': unassigned_users_list, 
            })
    # Add existed user to te group
    elif request.POST.get('action') == 'add':
        add_existed_user(request)
        # try:
        week_list = WOR_date.objects.all()
        user_list = UserModel.objects.filter(groups = UserModel.objects.get(id = request.user.id).groups.first())
        unassigned_users_list = UserModel.objects.filter(groups = None)
        current_week = datetime.datetime.now().strftime("%V")
        if current_week[0] == "0":
            current_week = int(current_week) % 10
        else:
            current_week = int(current_week)

        week_roles = WeekAttendanceRoleManager.objects.filter(users_group = UserModel.objects.get(id = request.user.id).groups.first())
        current_week_roles = WeekAttendanceRoleManager.objects.filter(
            users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
            week_id = WOR_date.objects.get(week_number = current_week)
            )
            
        return render(request, 'account/facilitator_list.html', {
        'users': user_list, 
        'current_week': current_week, 
        'week_list' :  week_list,
        'week_roles' : week_roles,
        })
        # except:
        #     return render(request, 'account/facilitator_list.html')
    # Remove user from the group
    elif request.POST.get('action') == 'remove':
        user_removal(request)
        try:
            week_list = WOR_date.objects.all()
            user_list = UserModel.objects.filter(groups = UserModel.objects.get(id = request.user.id).groups.first())
            unassigned_users_list = UserModel.objects.filter(groups = None)
            current_week = datetime.datetime.now().strftime("%V")
            if current_week[0] == "0":
                current_week = int(current_week) % 10
            else:
                current_week = int(current_week)

            week_roles = WeekAttendanceRoleManager.objects.filter(users_group = UserModel.objects.get(id = request.user.id).groups.first())
            current_week_roles = WeekAttendanceRoleManager.objects.filter(
                users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
                week_id = WOR_date.objects.get(week_number = current_week)
                )
            return render(request, 'account/facilitator_list.html', {
            'users': user_list, 
            'current_week': current_week, 
            'week_list' :  week_list,
            'week_roles' : week_roles,
            })
        except:
            return render(request, 'account/facilitator_list.html')
    # Update facilitators roles list
    elif request.POST.get('action') == 'update':
            import json
            from django.http import JsonResponse
            wor_leader_update_list =  json.loads(request.POST.get('wor_leaders_list'))  
            wor_engager_update_list = json.loads(request.POST.get('wor_engagers_list'))
            responce ={
                "user_id":'',
                "week":''
            }
            try:
                wor_leader_update_week = wor_leader_update_list['week'].split(',')
            except:
                wor_leader_update_week = ""
            try:
                wor_leader_update_id = wor_leader_update_list['user_id'].split(',')
            except:    
                wor_leader_update_id =""

            for i in range(len(wor_leader_update_id)):
                try:
                    week_for_update = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = wor_leader_update_week[i]), users_group = UserModel.objects.get(id = request.user.id).groups.first())
                    week_for_update.wor_leader = UserModel.objects.get(pk = int(wor_leader_update_id[i]))
                    week_for_update.save()
                except:
                    pass
            
            try:
                wor_engager_update_week = wor_engager_update_list['week'].split(',')
            except:
                wor_engager_update_week = ""
            try:
                wor_engager_update_id = wor_engager_update_list['user_id'].split(',')
            except:    
                wor_engager_update_id =""
            for i in range(len(wor_engager_update_id)):
                try:
                    week_for_update = WeekAttendanceRoleManager.objects.get(week_id = WOR_date.objects.get(week_number = wor_engager_update_week[i]), users_group = UserModel.objects.get(id = request.user.id).groups.first())
                    week_for_update.wor_engager = UserModel.objects.get(pk = int(wor_engager_update_id[i]))
                    week_for_update.save()
                except:
                    pass

            return JsonResponse(responce)
    try:
        week_list = WOR_date.objects.all()
        user_list = UserModel.objects.filter(groups = UserModel.objects.get(id = request.user.id).groups.first())
        unassigned_users_list = UserModel.objects.filter(groups = None)
        current_week = datetime.datetime.now().strftime("%V")
        if current_week[0] == "0":
            current_week = int(current_week) % 10
        else:
            current_week = int(current_week)

        week_roles = WeekAttendanceRoleManager.objects.filter(users_group = UserModel.objects.get(id = request.user.id).groups.first())
        current_week_roles = WeekAttendanceRoleManager.objects.filter(
            users_group = UserModel.objects.get(id = request.user.id).groups.first(), 
            week_id = WOR_date.objects.get(week_number = current_week)
            )
            
        return render(request, 'account/facilitator_settings.html', {
        'users': user_list, 
        'unassigned_users_list': unassigned_users_list,
        'current_week': current_week, 
        'week_list' :  week_list,
        'week_roles' : week_roles,
        'current_week_roles': current_week_roles
        })
    except:
        return render(request, 'account/facilitator_settings.html')

def user_removal(request):
    user_to_remove_id = request.POST.get('user_to_remove')
    user = UserModel.objects.get(pk = user_to_remove_id)
    user.groups.clear()
    user.save()
    time.sleep(2)
    user_calendar_update(request)
    this_group_action_list = ActionTaskManagerModel.objects.all()
    for action in this_group_action_list:
        try:
            action.assigned_user.remove(UserModel.objects.get(pk = user_to_remove_id))
        except:
            pass

def add_existed_user(request): 
    user_to_add_id = request.POST.get('user_to_add')
    user = UserModel.objects.get(pk = user_to_add_id)
    user.groups.add(UserModel.objects.get(id = request.user.id).groups.first())
    user.save()
    time.sleep(2)
    user_calendar_update(request)

from django.utils import timezone

def user_calendar_update(request):
    current_user = UserModel.objects.get(id=request.user.id)
    user_group = current_user.groups.first()

    current_date = timezone.now()
    current_week = WOR_date.objects.get(week_number= current_date.strftime("%V"))
    current_group_user_list = UserModel.objects.filter(groups=user_group)
    ready_selected = WeekAttendanceRoleManager.objects.get(week_id=current_week, users_group=user_group).wor_leader.id

    # Collect updates in a list
    updates = []

    for week in WOR_date.objects.filter(week_number__gte=current_week.week_number):
        for j in range(len(current_group_user_list)):
            if current_group_user_list[j].id == ready_selected:
                WeekAttendanceRole = WeekAttendanceRoleManager.objects.get(week_id=week, users_group=user_group)
                WeekAttendanceRole.wor_leader = current_group_user_list[j]
                WeekAttendanceRole.wor_engager = current_group_user_list[(j + 1) % len(current_group_user_list)]
                updates.append(WeekAttendanceRole)

                ready_selected = current_group_user_list[(j + 1) % len(current_group_user_list)].id
                break

    # Bulk update the changes
    if updates:
        WeekAttendanceRoleManager.objects.bulk_update(updates, ['wor_leader', 'wor_engager'])

    # Remove the time.sleep(2) if not needed
