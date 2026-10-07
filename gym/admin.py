from django.contrib import admin
from .models import Trainer, Member, Workout, Diet
from django.contrib import admin, messages

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
    def save_model(self, request, obj, form, change):
        if obj.trainer != obj.member.trainer:
            messages.warning(request,
            "Warning: This member does not belong to the selected trainer. Diet was not saved."
            )
            return
        super().save_model(request, obj, form, change)


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

    def save_model(self, request, obj, form, change):
        if obj.trainer != obj.member.trainer:
            messages.warning(request,
            "Warning: This member does not belong to the selected trainer. Diet was not saved."
            )
            return
        super().save_model(request, obj, form, change)