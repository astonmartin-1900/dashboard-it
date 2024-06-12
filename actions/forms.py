from django import forms
from .models import *

from django.contrib.admin import widgets
class DateInput(forms.DateInput):
    input_type = 'date'
class ActionCreateForm(forms.ModelForm):
    class Meta:
        model = ActionTaskManagerModel
        fields = [
            'issue_name',
            'action_text',
            'solution_text',
            'assigned_user',
            'deadline_date',
            'action_status'
        ]
        widgets = {
            'deadline_date': DateInput(),
        }
