from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from authapp.models import UserModel
from .forms import ImprovementCreateForm
from django.http import JsonResponse
import datetime

# Create your views here.
@login_required
def improvements(request):
    current_user = UserModel.objects.get(id=request.user.id)
    current_user_group = current_user.groups.first()

    improvement_create_form = ImprovementCreateForm(request.POST)
    improvements_list = ImprovementsTaskManagerModel.objects.filter(group=current_user_group)
    user_profile_images = UserModel.objects.filter(groups=current_user_group)

    response_data = {}

    if request.method == "GET" and request.GET.get('action') == 'get_data':
        improvement_pk = request.GET.get("improvement_pk", 1)
        selected_improvement = ImprovementsTaskManagerModel.objects.get(id = improvement_pk)
        
        response_data['improvement_pk'] = improvement_pk
        response_data['title'] = selected_improvement.title
        response_data['description'] = selected_improvement.description

        response_data['status'] = selected_improvement.status
        response_data['assigned_users'] = selected_improvement.get_assigned_user()
        response_data['start_date'] = selected_improvement.start_date
        response_data['deadline_date'] = selected_improvement.deadline_date

        return JsonResponse(response_data)
    
    if request.POST.get('action') == 'add':
        improvement_title = request.POST.get('title')
        improvement_description = request.POST.get('description')
        selected_status= request.POST.get('status')

        start_date = request.POST.get('start_date')
        deadline_date = request.POST.get('deadline_date')
        
        assigned_user_list = str(request.POST.get('assigned_users'))
        assigned_user = assigned_user_list.split(',')

        new_improvement = ImprovementsTaskManagerModel.objects.create(
                creation_date = datetime.datetime.now(),

                title = improvement_title,
                description  = improvement_description,
                status = selected_status, 

                start_date = start_date,
                deadline_date = deadline_date,
                group = UserModel.objects.get(id = request.user.id).groups.first()
            )
        for user in assigned_user:
            new_improvement.assigned_user.add(user)
        new_improvement.save()
        
        return render(request, 'improvements/templates/improvement_listing.html', {'improvements': improvements_list, 'create_form': improvement_create_form, 'user_profile_list': user_profile_images})

    if request.POST.get('action') == 'edit':
        #Collecting data form response
        improvement_pk = request.POST.get('improvement_pk')
        improvement_title = request.POST.get('title')
        improvement_description = request.POST.get('description')
        selected_status= request.POST.get('status')
        start_date = request.POST.get('start_date')
        deadline_date = request.POST.get('deadline_date')
        
        #Updating improvement(instance) data
        instance = ImprovementsTaskManagerModel.objects.get(id = improvement_pk)
        instance.title=improvement_title
        instance.description=improvement_description
        instance.status=selected_status
        instance.start_date=start_date
        instance.deadline_date=deadline_date

        #Connecting user with improvement
        assigned_user_list = request.POST.get('assigned_users')
        assigned_user = assigned_user_list.split(',')
        try:
            for user in assigned_user:
                instance.assigned_user.add(user)
        except:
            changed = False
        #Removing user from improvement connections
        unassigned_user_list = request.POST.get('unassigned_users')
        if unassigned_user_list != "":
            unassigned_user = unassigned_user_list.split(',')
            try:
                for user in unassigned_user:
                    instance.assigned_user.remove(user)
            except:
                changed = False
        instance.save()
        return render(request, 'improvements/templates/improvement_listing.html', {'improvements': improvements_list, 'create_form': improvement_create_form, 'user_profile_list': user_profile_images})
    return render(request, 'improvements/templates/improvement.html', {'improvements': improvements_list, 'create_form': improvement_create_form, 'user_profile_list': user_profile_images})

def change_status(request, pk):
    item_id = request.POST.get("item")
    items = ImprovementsTaskManagerModel.objects.get(id=pk)
    changed = True
    if "to_do" in request.POST:
        try:
            ImprovementsTaskManagerModel.objects.filter(id=pk).update(status="to_do")
        except:
            changed = False
    elif "in_progress" in request.POST:
        try:
            ImprovementsTaskManagerModel.objects.filter(id=pk).update(status='in_progress')
        except:
            changed = False
    elif "review" in request.POST:
        try:
            ImprovementsTaskManagerModel.objects.filter(id=pk).update(status='review')
        except:
            changed = False
    else:
        try:
            ImprovementsTaskManagerModel.objects.filter(id=pk).update(status="done")
        except:
            changed = False
    if changed:
        updated_improvement = ImprovementsTaskManagerModel.objects.get(id=pk)
        updated_improvement.save()
    return redirect('/improvements')

def improvement_edit(request, pk):
    instance = ImprovementsTaskManagerModel.objects.get(id=pk)
    improvements_update_form = ImprovementCreateForm(request.POST or None, instance=instance)
    if improvements_update_form.is_valid():
        improvements_update_form.save()
        return redirect('/improvements')
    return render(request, 'improvements/templates/edit_improvement.html', {'update_form': improvements_update_form, })