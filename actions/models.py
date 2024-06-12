from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from authapp.models import UserModel

# Create your models here.

class ActionTaskManagerModel(models.Model):
    STATUS_CHOICES = (
        ('draft', 'DRAFT'),
        ('canceled', 'CANCELED'),
        ('completed', 'COMPLETED'),
    )
    objects = models.Manager()
    creation_date = models.DateField(auto_now_add=True, verbose_name="Creation date")
    issue_name = models.CharField(max_length=255, blank=False, verbose_name="Issue title")
    action_text = models.TextField(blank=True, verbose_name="Issue description")
    solution_text = models.TextField(blank=True, verbose_name="Issue action")
    assigned_user = models.ManyToManyField(
        UserModel,
        through='AssignedToAction',
        verbose_name="Assigned"
    )
    deadline_date = models.DateField(verbose_name="Deadline date")
    action_status = models.CharField(max_length=9, choices=STATUS_CHOICES, default='draft')
    action_group = models.ForeignKey(Group, blank=False, default="1", on_delete=models.CASCADE, verbose_name="Action groups")

    def __str__(self):
        return self.issue_name

    def get_assigned_user(self):
        return ",".join([str(p.pk) for p in self.assigned_user.all()])
    class Meta:
        verbose_name = 'Action'
        verbose_name_plural = 'Actions'
        ordering = ['-action_status', '-id']

#model that used for action assignment
class AssignedToAction(models.Model):
    person = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    action = models.ForeignKey(ActionTaskManagerModel, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.action

    class Meta:
        ordering = ('action',)