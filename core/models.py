from django.db import models

# Create your models here.
class MeetingMinutes(models.Model):

    date=models.DateField(null=False, blank=False)
    location=models.CharField(null=False, blank=False)
    agenda=models.CharField(null=False, blank=False)
    discussion= models.TextField(null=True, blank=True)

    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)

    class Meta:
        verbose_name= 'MeetingMinutes'

    def __str__(self):
        return str(self.pk)    