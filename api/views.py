from django.core import serializers
from django.http import HttpResponse
from api.models import Board, Reading

def boards(request):

    if request.method == 'GET':
        boards = Board.objects.all()
        data = serializers.serialize('json', boards)
        return HttpResponse(data, content_type='application/json')
    

def readings(request, board_id):

    if request.method == 'GET':
        readings = Reading.objects.filter(board_id=board_id)
        data = serializers.serialize('json', readings)
        return HttpResponse(data, content_type='application/json')
