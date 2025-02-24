import base64
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from api.models import Board, Reading
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError, DataError
from datetime import timedelta
from django.urls import reverse
from django.utils.timezone import now
from django.db.models import Avg, Q, Min, Max
import json

User = get_user_model()


def authenticate_user(request):
    """Extract and authenticate user from the Authorization header."""
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Basic "):
        return None, JsonResponse(
            {"error": "Unauthorized"},
            status=401,
            headers={"WWW-Authenticate": 'Basic realm="Restricted"'},
        )

    try:
        encoded_credentials = auth_header.split(" ")[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":", 1)
    except (ValueError, base64.binascii.Error):
        return None, JsonResponse({"error": "Invalid authorization header"}, status=400)

    user = authenticate(username=username, password=password)
    if user is None:
        return None, JsonResponse(
            {"error": "Invalid credentials"},
            status=401,
            headers={"WWW-Authenticate": 'Basic realm="Restricted"'},
        )

    return user, None


def boards(request):
    if request.method == "GET":
        boards = Board.objects.all()
        data = serializers.serialize("json", boards)
        return HttpResponse(data, content_type="application/json")


def readings(request, board_id):
    if request.method == "GET":
        readings = Reading.objects.filter(board_id=board_id)
        data = serializers.serialize("json", readings)
        return HttpResponse(data, content_type="application/json")


def board_detail(request, board_id=None):
    if board_id is None:
        first_board = Board.objects.first()
        if first_board:
            return redirect(reverse('board_detail', args=[first_board.id]))
        else:
            return redirect('/')

    boards = Board.objects.all()

    last_24_hours = now() - timedelta(hours=24)

    board = get_object_or_404(
        Board.objects.annotate(
            avg_temp_24h=Avg(
                "readings__temperature",
                filter=Q(readings__timestamp__gte=last_24_hours),
            ),
            min_temp_24h=Min(
                "readings__temperature",
                filter=Q(readings__timestamp__gte=last_24_hours),
            ),
            max_temp_24h=Max(
                "readings__temperature",
                filter=Q(readings__timestamp__gte=last_24_hours),
            ),
        ),
        id=board_id,
    )

    reading_qs = board.readings.filter(timestamp__gte=last_24_hours).order_by(
        "-timestamp"
    )

    readings = list(
        reading_qs.values(
            "timestamp",
            "temperature",
            "humidity",
            "moisture_a",
            "moisture_b",
            "moisture_c",
        )
    )

    first_reading, last_reading = reading_qs.first(), reading_qs.last()

    if first_reading and last_reading:
        moisture_differences = {
            "Plant A": first_reading.moisture_a - last_reading.moisture_a,
            "Plant B": first_reading.moisture_b - last_reading.moisture_b, 
            "Plant C": first_reading.moisture_c - last_reading.moisture_c
        }
    else:
        moisture_differences = None

    context = {
        "user_boards": boards,
        "board": board,
        "readings": reading_qs,
        "readings_dict": readings,
        "moisture_difference": moisture_differences,
    }

    return render(request, "dashboard.html", context=context)


@csrf_exempt
@require_POST
def submit_reading(request):
    """Handles device readings submission."""
    user, auth_error = authenticate_user(request)
    if auth_error:
        return auth_error

    try:
        reading_data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON payload"}, status=400)

    uid = reading_data.get("uid")
    nickname = reading_data.get("nickname")
    timestamp = parse_datetime(reading_data.get("timestamp"))
    readings = reading_data.get("readings", {})

    if not uid:
        return JsonResponse({"error": "Missing board UID"}, status=400)

    board, _ = Board.objects.get_or_create(
        user=user, uid=uid, defaults={"nickname": nickname}
    )

    try:
        Reading.objects.create(board=board, timestamp=timestamp, **readings)
        return HttpResponse(status=201)
    except (IntegrityError, DataError) as e:
        return JsonResponse({"error": str(e)}, status=400)
