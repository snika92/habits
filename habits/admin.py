from django.contrib import admin

from .models import Habit, Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("title", "owner")
    search_fields = ("title",)
    list_filter = ("owner",)


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        "action",
        "owner",
        "place",
        "last_execution_time",
        "is_pleasant_habit",
        "period",
        "is_public",
    )
    search_fields = ("action",)
    list_filter = ("owner", "place", "is_pleasant_habit", "period", "is_public")
