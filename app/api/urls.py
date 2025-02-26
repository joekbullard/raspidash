from django.urls import path
from api.views import board_detail, submit_reading

urlpatterns = [
    path('', board_detail),
    path('<int:board_id>/', board_detail, name="board_detail"),
    path('submit-reading/', submit_reading)
]