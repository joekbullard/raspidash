import base64
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from api.models import Board, Reading
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_datetime
from django.db import IntegrityError, DataError
from datetime import timedelta
from django.utils.timezone import now
import json


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


def board_detail(request, board_id):
    if request.method == "GET":
        last_3_days = now() - timedelta(days=3)
        board = get_object_or_404(Board, id=board_id)
        readings = [
            {
                "timestamp": r.timestamp,
                "temperature": r.temperature,
                "humidity": r.humidity,
                "luminance": r.luminance,
                "moisture_a": r.moisture_a,
                "moisture_b": r.moisture_b,
                "moisture_c": r.moisture_c,
            }
            for r in Reading.objects.filter(board__id=board_id, timestamp__gte=last_3_days)
        ]

        context = {"board": board, "readings": readings}

        return render(request, "dashboard.html", context=context)


@csrf_exempt
@require_POST
def submit_reading(request):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Basic "):
        return JsonResponse(
            {"error": "Unauthorized"},
            status=401,
            headers={"WWW-Authenticate": 'Basic realm="Restricted"'},
        )

    try:
        encoded_credentials = auth_header.split(" ")[1]
        decoded_credentials = base64.b64decode(encoded_credentials).decode("utf-8")
        username, password = decoded_credentials.split(":", 1)
    except (ValueError, base64.binascii.Error):
        return JsonResponse({"error": "Invalid authorization header"}, status=400)

    user = authenticate(username=username, password=password)
    if user is None:
        return JsonResponse(
            {"error": "Invalid credentials"},
            status=401,
            headers={"WWW-Authenticate": 'Basic realm="Restricted"'},
        )

    try:
        reading = json.loads(request.body)
    except json.JSONDecodeError as e:
        return JsonResponse({"error": e})

    uid = reading.get("uid")
    nickname = reading.get("nickname")

    if not uid:
        return JsonResponse({"error": "Missing board UID"}, status=400)

    board, created = Board.objects.get_or_create(
        user=request.auth, uid=uid, nickname=nickname
        )
    timestamp = parse_datetime(reading.get("timestamp"))
    readings = reading.get("readings", {})
    
    try:
        Reading.objects.create(board=board, timestamp=timestamp, **readings)
        return HttpResponse(status=201)
    except IntegrityError as e:
        return JsonResponse({"error": e}, status=400)
    except DataError as e:
        return JsonResponse({"error": e}, status=400)
