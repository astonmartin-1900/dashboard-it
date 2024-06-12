from django.contrib import admin
from .models import ImprovementsTaskManagerModel, AssignedToImprovement

# Register your models here.
admin.site.register(ImprovementsTaskManagerModel)
admin.site.register(AssignedToImprovement)