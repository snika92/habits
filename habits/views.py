from datetime import datetime

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit, Place
from habits.paginators import CustomPagination
from habits.serializers import HabitSerializer, PlaceSerializer
from users.permissions import IsModerator, IsOwner


class PlaceViewSet(ModelViewSet):
    serializer_class = PlaceSerializer

    def get_queryset(self, *args, **kwargs):
        if (
            self.request.user.groups.filter(name="moderators")
            or self.request.user.is_superuser
        ):
            return Place.objects.all()
        return Place.objects.filter(owner=self.request.user.id)

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = [~IsModerator]
        elif self.action in ["retrieve", "update"]:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == "destroy":
            self.permission_classes = [~IsModerator | IsOwner]
        return super().get_permissions()

    def perform_create(self, serializer):
        new_place = serializer.save()
        new_place.owner = self.request.user
        new_place.save()


class HabitCreateApiView(CreateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [~IsModerator, IsAuthenticated]

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.owner = self.request.user
        new_habit.last_execution_time = datetime.now().date()
        new_habit.save()


class HabitListApiView(ListAPIView):
    pagination_class = CustomPagination
    serializer_class = HabitSerializer
    permission_classes = [IsModerator | IsOwner, IsAuthenticated]

    def get_queryset(self, *args, **kwargs):
        if (
            self.request.user.groups.filter(name="moderators")
            or self.request.user.is_superuser
        ):
            return Habit.objects.all()
        return Habit.objects.filter(owner=self.request.user.id)

    filterset_fields = ("place", "is_pleasant_habit", "period", "is_public")
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ("action",)
    search_fields = ("action",)


# Список публичных привычек
class PublicHabitListApiView(ListAPIView):
    queryset = Habit.objects.filter(is_public=True)
    pagination_class = CustomPagination
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)

    filterset_fields = ("place", "is_pleasant_habit", "period")
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ("action",)
    search_fields = ("action",)


class HabitRetrieveApiView(RetrieveAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class HabitUpdateApiView(UpdateAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class HabitDestroyApiView(DestroyAPIView):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, ~IsModerator | IsOwner]
