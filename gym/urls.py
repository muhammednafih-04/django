from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register("trainers",views.TrainerViewSet,basename='trainer')
router.register("members",views.MemberViewSet,basename='members')
router.register("workouts",views.WorkoutViewSet,basename='workout')
router.register('diets',views.DietViewSet,basename='diets')


urlpatterns = [
    path('admin_dashboard/',views.admin_dashboard,name='admin_dashboard'),

    path('trainer_dash/',views.trainer_dashboard,name='trainer_dash'),

    path('api/',include(router.urls)),

    path(
    'trainer-login/',
    views.trainer_login,
    name='trainer_login'
),
    path(
    'trainer-logout/',
    views.trainer_logout,
    name='trainer_logout'
),
    path(
    'admin-login/',
    views.admin_login,
    name='admin_login'
),
    path(
    'admin-logout/',
    views.admin_logout,
    name='admin_logout'
),
    path(
    'user-login/',
    views.user_login,
    name='user_login'
),
    path(
    'user-dashboard/',
    views.user_dashboard,
    name='user_dashboard'
),
    path(
    'user-logout/',
    views.user_logout,
    name='user_logout'
),
]