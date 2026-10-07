from django.shortcuts import render,redirect
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from .models import Trainer, Member, Workout, Diet
from .serializers import (
    TrainerSerializer,
    MemberSerializer,
    WorkoutSerializer,
    DietSerializer
)
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# -------------------------
# TRAINER API
# -------------------------
class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer


# -------------------------
# MEMBER API
# -------------------------
class MemberViewSet(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        try:
            trainer = Trainer.objects.get(
                user=self.request.user
            )

            return Member.objects.filter(
                trainer=trainer
            )
        except Trainer.DoesNotExist:

            return Member.objects.none()


    def perform_create(self, serializer):

        trainer = Trainer.objects.get(
            user=self.request.user)

        serializer.save(
            trainer=trainer)

# -------------------------
# WORKOUT API
# -------------------------
class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        try:
            trainer = Trainer.objects.get(
                user=self.request.user
            )

            return Workout.objects.filter(
                trainer=trainer
            )

        except Trainer.DoesNotExist:

            return Workout.objects.none()

    def perform_create(self, serializer):

        trainer = Trainer.objects.get(
            user=self.request.user
        )

        member = serializer.validated_data['member']

        # IMPORTANT CHANGE
        if member.trainer != trainer:
            raise PermissionDenied(
                "This member belongs to another trainer."
            )

        serializer.save(
            trainer=trainer
        )

    # IMPORTANT CHANGE
    def perform_update(self, serializer):

        trainer = Trainer.objects.get(
            user=self.request.user
        )

        member = serializer.validated_data.get(
            'member',
            serializer.instance.member
        )

        # IMPORTANT CHANGE
        if member.trainer != trainer:
            raise PermissionDenied(
                "This member belongs to another trainer."
            )

        serializer.save(
            trainer=trainer
        )
# -------------------------
# DIET API
# -------------------------
class DietViewSet(viewsets.ModelViewSet):
    serializer_class = DietSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        try:
            trainer = Trainer.objects.get(
                user=self.request.user
            )

            return Diet.objects.filter(
                trainer=trainer
            )

        except Trainer.DoesNotExist:

            return Diet.objects.none()

    def perform_create(self, serializer):

        trainer = Trainer.objects.get(
            user=self.request.user
        )

        member = serializer.validated_data['member']

        if member.trainer != trainer:
            raise PermissionDenied(
                "You can only add diets for your own users."
            )

        serializer.save(
            trainer=trainer
        )

    # IMPORTANT CHANGE
    def perform_update(self, serializer):

        trainer = Trainer.objects.get(
            user=self.request.user
        )

        member = serializer.validated_data.get(
            'member',
            serializer.instance.member
        )

        if member.trainer != trainer:
            raise PermissionDenied(
                "You can only manage diets for your own users."
            )

        serializer.save(
            trainer=trainer
        )
#-----login------#

def admin_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None and user.is_staff:

            login(request, user)

            return redirect('admin_dashboard')

        else:

            return render(
                request,
                'gym/admin_login.html',
                {
                    'error': 'Invalid admin username or password.'
                }
            )

    return render(
        request,
        'gym/admin_login.html'
    )

# -------------------------
# ADMIN DASHBOARD
# -------------------------

@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        return redirect('admin_login')

    trainer_count = Trainer.objects.count()
    member_count = Member.objects.count()
    workout_count = Workout.objects.count()
    diet_count = Diet.objects.count()
    
    recent_members = Member.objects.select_related(
        'user', 'trainer'
    ).order_by('-id')[:5]

    recent_workouts = Workout.objects.select_related(
        'member', 'trainer'
    ).order_by('-id')[:5]

    recent_diets = Diet.objects.select_related(
        'member', 'trainer'
    ).order_by('-id')[:5]


    context = {
        'trainer_count': trainer_count,
        'member_count': member_count,
        'workout_count': workout_count,
        'diet_count': diet_count,

        'recent_members': recent_members,
        'recent_workouts': recent_workouts,
        'recent_diets': recent_diets,
    }
    

    return render(
        request,
        'gym/admin_dashboard.html',
        context
    )


@login_required(login_url='trainer_login')
def trainer_dashboard(request):

    try:
        trainer = Trainer.objects.get(user=request.user)

    except Trainer.DoesNotExist:
        return redirect('trainer_login')

    member_count = Member.objects.filter(
        trainer=trainer
    ).count()

    workout_count = Workout.objects.filter(
        trainer=trainer
    ).count()

    diet_count = Diet.objects.filter(
        trainer=trainer
    ).count()

    context = {
        'trainer': trainer,
        'member_count': member_count,
        'workout_count': workout_count,
        'diet_count': diet_count,
    }

    return render(
        request,
        'gym/trainer_dash.html',
        context
    )

def trainer_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:
                Trainer.objects.get(user=user)

                login(request, user)

                return redirect('trainer_dash')

            except Trainer.DoesNotExist:

                return render(
                    request,
                    'gym/trainer_login.html',
                    {
                        'error': 'This account is not registered as a trainer.'
                    }
                )

        else:

            return render(
                request,
                'gym/trainer_login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(
        request,
        'gym/trainer_login.html'
    )

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Check that this user is a Member
            try:
                Member.objects.get(user=user)

                login(request, user)

                return redirect('user_dashboard')

            except Member.DoesNotExist:

                return render(
                    request,
                    'gym/user_login.html',
                    {
                        'error': 'This account is not registered as a user.'
                    }
                )

        else:

            return render(
                request,
                'gym/user_login.html',
                {
                    'error': 'Invalid username or password.'
                }
            )

    return render(
        request,
        'gym/user_login.html'
    )


@login_required(login_url='user_login')
def user_dashboard(request):
    try:
        member = Member.objects.get(
            user=request.user
        )

        workouts = Workout.objects.filter(
            member=member
        )

        diets = Diet.objects.filter(
            member=member
        )

        context = {
            'trainer':member.trainer,
            'member': member,
            'workouts': workouts,
            'diets': diets,
        }

        return render(
            request,
            'gym/user_dashboard.html',
            context
        )

    except Member.DoesNotExist:

        logout(request)

        return redirect('user_login')

#.......logout......
def trainer_logout(request):
    logout(request)
    return redirect('trainer_login')

def admin_logout(request):
    logout(request)
    return redirect('admin_login')

def user_logout(request):
    logout(request)
    return redirect('user_login')

def home(request):
    return render(request,'gym/home.html')
