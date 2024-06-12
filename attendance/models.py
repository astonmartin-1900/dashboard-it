from datetime import datetime
import calendar
from django.db import models

# Create your models here.
from authapp.models import UserModel
from django.contrib.auth.models import Group

# Create your models here.
class WOR_date (models.Model):
    start_date  =models.DateField(default=datetime.now,blank=True, verbose_name="week start date")
    end_date = models.DateField(default=datetime.now,blank=True, verbose_name="week end date")
    week_number = models.IntegerField(default="0", verbose_name="Week")
    
    def __str__(self):
        return "Week#"+str(self.week_number);
    class Meta:
        ordering = ['week_number']

class WeekAttendanceRoleManager(models.Model):
    week_id =  models.ForeignKey(WOR_date, on_delete=models.CASCADE)
    users_group = models.ForeignKey(Group, blank=False, default="1", on_delete=models.CASCADE, verbose_name="Role`s group")
    wor_leader = models.ForeignKey(UserModel, related_name='wor_leader', on_delete=models.CASCADE, verbose_name="WOR Learder")
    wor_engager = models.ForeignKey(UserModel, related_name='wor_engager', on_delete=models.CASCADE, verbose_name="WOR Engager")

    def __str__(self):
        return "Group#"+ str(self.users_group) +"; Week#"+str(self.week_id.week_number)

    class Meta:
        ordering = ['week_id']

class AttendanceManagerModel(models.Model):
    USER_STATUS = (
        ('present', 'PRESENT'),
        ('absent', 'ABSENT'),
        ('excused', 'EXCUSED'),
        ('on_vacation', 'ON_VACATION'),
        ('comes_later', 'COMES_LATER')
    )
    date = models.ForeignKey(WOR_date, on_delete=models.CASCADE)
    person = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    user_status = models.CharField(max_length=11, choices=USER_STATUS, default='present')

    def __str__(self):
        return "Week#"+str(self.date.week_number) +' / ' +  self.person.username

    class Meta:
        ordering = ['date']
