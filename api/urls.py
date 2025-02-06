from django.urls import path
from api.views import boards, readings

urlpatterns = [
    path('boards/', boards),
    path('boards/<int:board_id>/readings', readings)
]