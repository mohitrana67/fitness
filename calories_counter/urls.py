from django.urls import path
from calories_counter.views import(
    addFood as af
)

urlpatterns = [
    path('add_food/',af, name="addUser"),
]