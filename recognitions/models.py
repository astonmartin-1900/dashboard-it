from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

from authapp.models import UserModel

# Create your models here.
class RecognitionManagerModel(models.Model):
    user_profile = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    initiative_value = models.IntegerField(default="0", verbose_name="Initiative")
    understand_value = models.IntegerField(default="0", verbose_name="Understanding Business Environment")
    practice_value = models.IntegerField(default="0", verbose_name="Practice what you Preach")
    result_focus_value = models.IntegerField(default="0", verbose_name="Result focus")
    know_yourself_value = models.IntegerField(default="0", verbose_name="Know Yourself")
    cooperation_value = models.IntegerField(default="0", verbose_name="Proactive Cooperation")
    all_stars_value = models.IntegerField(default="0", verbose_name="All Stars value")
    total_stars = models.IntegerField(default="0", verbose_name="Total stars")

    def __str__(self):
        return self.user_profile.username
    
    class Meta:
        ordering = ['user_profile']