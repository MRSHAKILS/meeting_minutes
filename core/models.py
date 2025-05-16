from django.db import models

# Create your models here.
class MeetingMinutes(models.Model):

    date=models.DateField(null=False, blank=False)
    location=models.CharField(null=False, blank=False)
    agenda=models.CharField(null=False, blank=False)
    discussion= models.TextField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    hosts = models.CharField(max_length=255, blank=True, null=True)
    co_hosts = models.CharField(max_length=255, blank=True, null=True)
    guests = models.TextField(blank=True, null=True)
    written_by = models.CharField(max_length=100, blank=True, null=True)
    total_attendees = models.PositiveIntegerField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        verbose_name= 'MeetingMinutes'

    def __str__(self):
        return str(self.pk)    