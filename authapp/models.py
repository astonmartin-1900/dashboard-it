from datetime import datetime  
from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractUser, Group
# Create your models here.


class UserModel(AbstractUser):
    id = models.AutoField(primary_key=True)
    objects = UserManager()
    user_image = models.ImageField(blank=False, upload_to="profile_image/", default='default_image/default_user_image.png',
                                   verbose_name="Profile image")
    user_position = models.CharField(blank=True, max_length=255, verbose_name="User position")
    user_about = models.TextField(blank=True, verbose_name="About you")

    class Meta:
        ordering = ['first_name']

class GroupAdmin(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.ForeignKey(UserModel, on_delete=models.CASCADE, verbose_name="Group admin")
    group = models.ForeignKey(Group, blank=True, default="1", on_delete=models.CASCADE, verbose_name="Group")
    group_time_zone = models.IntegerField(default="2", verbose_name="Time zone")

class Meta:
    permission =[( "edit_facilitators", "Can edit facilitators",)]