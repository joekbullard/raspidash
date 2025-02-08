from django.db import models
from django.conf import settings


class Board(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40)
    uid = models.CharField(max_length=16, unique=True)

    def __repr__(self):
        return self.nickname


class Reading(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="readings")
    timestamp = models.DateTimeField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    pressure = models.FloatField()
    luminance = models.FloatField()
    moisture_a = models.FloatField()
    moisture_b = models.FloatField()
    moisture_c = models.FloatField()

    class Meta:
        ordering = ["timestamp"]