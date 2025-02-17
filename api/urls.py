from django.urls import path
from api.views import boards, board_detail, submit_reading

urlpatterns = [
    path('boards/', boards),
    path('dashboard/', board_detail),
    path('dashboard/<int:board_id>/', board_detail, name="board_detail"),
    path('submit-reading/', submit_reading)
]