from django.http import JsonResponse
from api.models import Board, Reading

def boards_view(request):
    boards = Board.objects.all()
    return JsonResponse(boards)


