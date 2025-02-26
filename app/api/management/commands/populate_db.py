from django.core.management.base import BaseCommand
from django.utils.timezone import now, timedelta
import random
from api.models import Board, Reading  # Adjust your app name
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Populate the database with test readings every 15 minutes for the last 24 hours"

    def handle(self, *args, **kwargs):
        user, _ = User.objects.get_or_create(username="testuser", defaults={"email": "test@example.com"})
        board, _ = Board.objects.get_or_create(user=user, nickname="Test Board", uid="TEST1234")

        start_time = now() - timedelta(hours=24)
        readings = []
        
        for i in range(96):  # 4 readings per hour * 24 hours
            readings.append(Reading(
                board=board,
                timestamp=start_time + timedelta(minutes=15 * i),
                temperature=random.uniform(15, 30),
                humidity=random.uniform(30, 80),
                pressure=random.uniform(980, 1050),
                luminance=random.uniform(100, 1000),
                moisture_a=random.uniform(10, 50),
                moisture_b=random.uniform(10, 50),
                moisture_c=random.uniform(10, 50),
            ))

        Reading.objects.bulk_create(readings)
        self.stdout.write(self.style.SUCCESS("Successfully populated database with readings"))
