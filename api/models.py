from django.db import models
from django.conf import settings


class Board(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=40)
    uid = models.CharField(max_length=16)

    class Meta:
        unique_together = ('user', 'uid')

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

    def __repr__(self):
        return f"{self.board.nickname} - {self.timestamp}"
    
    def get_moisture_values(self):
        """
        Returns moisture values with user-assigned plant names.
        """
        sensor_map = {s.sensor_slot: s.name for s in self.board.moisture_sensors.all()}
        return {
            sensor_map.get("A", "Moisture A"): self.moisture_a,
            sensor_map.get("B", "Moisture B"): self.moisture_b,
            sensor_map.get("C", "Moisture C"): self.moisture_c,
        }
    

class MoistureSensor(models.Model):
    class SensorName(models.TextChoices):
        SENSOR_A = 'A'
        SENSOR_B = 'B'
        SENSOR_C = 'C'
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="sensors")
    name = models.CharField(max_length=50)
    sensor_slot = models.CharField(max_length=1, choices=SensorName.choices)

    class Meta:
        unique_together = ('board', 'sensor_slot')

    def __repr__(self):
        return f"{self.name} ({self.sensor_slot})"
