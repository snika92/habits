from django.urls import path
from rest_framework.routers import SimpleRouter

from habits.apps import HabitsConfig
from habits.views import (HabitCreateApiView, HabitDestroyApiView,
                          HabitListApiView, HabitRetrieveApiView,
                          HabitUpdateApiView, PlaceViewSet)

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("places", PlaceViewSet)

urlpatterns = [
    path("", HabitListApiView.as_view(), name="habits_list"),
    path("<int:pk>/", HabitRetrieveApiView.as_view(), name="habit_retrieve"),
    path("create/", HabitCreateApiView.as_view(), name="habit_create"),
    path("<int:pk>/delete/", HabitDestroyApiView.as_view(), name="habit_delete"),
    path("<int:pk>/update/", HabitUpdateApiView.as_view(), name="habit_update"),
]

urlpatterns += router.urls
