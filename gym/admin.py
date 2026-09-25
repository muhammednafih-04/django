from django.contrib import admin
from .models import Trainer, Member, Workout, Diet


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'user',
        'email',
        'phone',
        'specialization'
    )

    search_fields = (
        'name',
        'email',
        'user__username'
    )


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'trainer',
        'age',
        'phone',
        'goal'
    )

    list_filter = (
        'trainer',
    )

    search_fields = (
        'user__username',
        'phone',
        'goal',
    )


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = (
        'exercise_name',
        'member',
        'trainer',
        'sets',
        'repetitions',
        'duration',
        'date'
    )

    list_filter = (
        'trainer',
        'date',
    )

    search_fields = (
        'exercise_name',
        'member__user__username',
    )


@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = (
        'meal_name',
        'member',
        'trainer',
        'calories',
        'date'
    )

    list_filter = (
        'trainer',
        'date',
    )

    search_fields = (
        'meal_name',
        'member__user__username',
    )
