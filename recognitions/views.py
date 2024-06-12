from django.core import serializers
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.urls import reverse 
from .models import RecognitionManagerModel
from authapp.models import UserModel
from django.http import JsonResponse
# Create your views here.
from django.template.loader import render_to_string
from django.http import JsonResponse

from django.contrib.auth.decorators import login_required
@login_required(login_url='/login/')
def recognition_page(request):
    user_group = request.user.groups.first()  # Get the user's group
    recognition_list = RecognitionManagerModel.objects.filter(user_profile__groups=user_group)
    user_list = UserModel.objects.filter(groups=user_group) if user_group else UserModel.objects.all()
    response_data = {}

    if request.POST.get('operation') == 'filter_by':
        ordering = "-" + str(request.POST.get('filter_id'))
        recognition_list = RecognitionManagerModel.objects.order_by(ordering, 'user_profile')
        return render(request, 'recognitions/templates/recognition_filter.html', {'recognition_list': recognition_list, 'user_list': user_list})

    if request.POST.get('action') == 'update_recognition':
        recognition_id = request.POST.get('recognition_id')
        initiative_value= request.POST.get('initiative_value')
        understand_value = request.POST.get('understand_value')
        practice_value = request.POST.get('practice_value')
        result_focus_value = request.POST.get('result_focus_value')
        know_yourself_value = request.POST.get('know_yourself_value')
        cooperation_value = request.POST.get('cooperation_value')

        response_data['recognition_id'] = recognition_id
        response_data['initiative_value'] = initiative_value
        response_data['understand_value'] = understand_value
        response_data['practice_value'] = practice_value
        response_data['result_focus_value'] = result_focus_value
        response_data['know_yourself_value'] = know_yourself_value
        response_data['cooperation_value'] = cooperation_value
        
        instance = RecognitionManagerModel.objects.get(pk = recognition_id)
        instance.initiative_value= initiative_value
        instance.understand_value=understand_value
        instance.practice_value=practice_value
        instance.result_focus_value=result_focus_value
        instance.know_yourself_value=know_yourself_value
        instance.cooperation_value=cooperation_value
        total_stars_count = int(initiative_value) + int(understand_value) + int(practice_value) + int(result_focus_value) + int(know_yourself_value) + int(cooperation_value)
        
        instance.total_stars = total_stars_count
        response_data['total_stars'] = total_stars_count
        instance.save()

        return JsonResponse(response_data)
    elif request.POST.get('operation') == 'add_star':
        content_id= request.POST.get('recognition_id')
        star_type = request.POST.get('type_of_star')

        content = RecognitionManagerModel.objects.get(pk = content_id)
        if star_type == 'initiative':
            content.initiative_value = content.initiative_value+1
        elif star_type == 'ube':
            content.understand_value = content.understand_value+1
        elif star_type == 'pwyp':
            content.practice_value = content.practice_value+1
        elif star_type == 'resut_focus':
            content.result_focus_value = content.result_focus_value+1
        elif star_type == 'know_yourself':
            content.know_yourself_value = content.know_yourself_value+1
        elif star_type == 'proactive_cooperation':
            content.cooperation_value = content.cooperation_value+1
        content.total_stars = content.total_stars+1
        content.save()

        return JsonResponse({'recognition_id':content_id,'type_of_star': star_type})
    # elif request.POST.get('operation') == 'add_all_stars':
    #     content_id= request.POST.get('recognition_id')
    #     content = RecognitionManagerModel.objects.get(pk = content_id)
    #     content.all_stars_value = content.all_stars_value+1
    #     content.save()

    #     return JsonResponse({'recognition_id':content_id,'all_stars_value': content.all_stars_value})
    
    return render(request, 'recognitions/templates/recognition.html', {'recognition_list': recognition_list, 'user_list': user_list})

@login_required(login_url='/login/')
def recognition_update(request):
    response_data = {}
    if request.POST.get('operation') == 'add_star':
        content_id= request.POST.get('recognition_id')
        star_type = request.POST.get('type_of_star')

        content = RecognitionManagerModel.objects.get(pk = content_id)
        if star_type == 'initiative':
                content.initiative_value = content.initiative_value+1
        else:
                content.initiative_value = content.initiative_value+1
        content.save()
        response_data['recognition_id'] = type(content_id)
        return JsonResponse(response_data)
    
    return render(request, 'recognitions/templates/recognition.html')
    