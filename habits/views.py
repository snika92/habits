from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit, Place
from habits.serializers import HabitSerializer, PlaceSerializer


class PlaceViewSet(ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer


class HabitCreateApiView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitListApiView(ListAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitRetrieveApiView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitUpdateApiView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer


class HabitDestroyApiView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
