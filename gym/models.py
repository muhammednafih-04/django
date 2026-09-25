from django.db import models
from django.contrib.auth.models import User


class Trainer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Member(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(
        Trainer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    name=models.CharField(max_length=100,default='')
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    goal = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class Workout(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    exercise_name = models.CharField(max_length=100)
    sets = models.IntegerField()
    repetitions = models.IntegerField()
    duration = models.IntegerField(help_text="Duration in minutes")
    date = models.DateField()

    def __str__(self):
        return self.exercise_name


class Diet(models.Model):
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=100)
    food_items = models.TextField()
    calories = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return self.meal_name
