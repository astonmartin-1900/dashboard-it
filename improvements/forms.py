from django import forms
from .models import *

from django.contrib.admin import widgets
class DateInput(forms.DateInput):
    input_type = 'date'
class ImprovementCreateForm(forms.ModelForm):
    class Meta:
        model = ImprovementsTaskManagerModel
        fields = [
            'title',
            'description',
            'assigned_user',
            'start_date',
            'deadline_date',
            'status',
        ]
        widgets = {
            'deadline_date': DateInput(),
            'start_date': DateInput(),
        }
