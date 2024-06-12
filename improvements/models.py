from django.db import models
from django.contrib.auth.models import Group
from django.conf import settings
from authapp.models import UserModel


class ImprovementsTaskManagerModel(models.Model):
    objects = models.Manager()
    creation_date = models.DateField(auto_now_add=True, verbose_name="Creation date")
    title = models.CharField(max_length=255, blank=False, verbose_name="Improvement title")
    description = models.TextField(blank=True, verbose_name="Improvement description")
    assigned_user = models.ManyToManyField(
        UserModel,
        through='AssignedToImprovement',
        verbose_name="Assigned"
    )
    start_date = models.DateField(verbose_name="Start date")
    deadline_date = models.DateField(verbose_name="Deadline date")
    STATUS_CHOICES = (
        ('to_do', 'TO DO'),
        ('in_progress', 'IN PROGRESS'),
        ('review', 'REVIEW'),
        ('done', 'DONE'),
    )
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='To Do')
    group = models.ForeignKey(Group, blank=False, default="1", on_delete=models.CASCADE, verbose_name="Improvement group")

    def __str__(self):
        return self.title

    def get_assigned_user(self):
        return ",".join([str(p.pk) for p in self.assigned_user.all()])

    class Meta:
        verbose_name = 'Improvement '
        verbose_name_plural = 'Improvements'
        ordering = ['status']

class AssignedToImprovement(models.Model):
    person = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    improvement = models.ForeignKey(ImprovementsTaskManagerModel, on_delete=models.CASCADE)

    def __unicode__(self):
        return self.improvement

    class Meta:
        ordering = ('improvement',)