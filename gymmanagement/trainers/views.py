from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from users.models import CustomUser
from trainees.models import Trainee, Activity, WeightLog
from .models import Trainer, Recommendation
from django.core.exceptions import ValidationError
from django.utils.timezone import now


class TrainerSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    age = forms.IntegerField()
    experience = forms.IntegerField()
    specialisation = forms.CharField(max_length=100)
    rate = forms.FloatField()
    start_time = forms.TimeField()
    end_time = forms.TimeField()


def trainer_signup(request):
    if request.method == 'POST':
        form = TrainerSignupForm(request.POST)
        if form.is_valid():
            try:
                # 1. Create the CustomUser with role='trainer'
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    role='trainer'
                )

                # 2. Create Trainer Profile
                trainer = Trainer(
                    user=user,
                    age=form.cleaned_data['age'],
                    experience=form.cleaned_data['experience'],
                    specialisation=form.cleaned_data['specialisation'],
                    rate=form.cleaned_data['rate'],
                    start_time=form.cleaned_data['start_time'],
                    end_time=form.cleaned_data['end_time'],
                )

                # 3. Run model validation (custom clean methods)
                trainer.full_clean()
                trainer.save()

                # 4. Log the user in and redirect
                login(request, user)
                return redirect('trainer_dashboard')

            except ValidationError as ve:
                user.delete()  # rollback if the profile fails
                form.add_error(None, ve.message_dict)

            except Exception as e:
                form.add_error(None, f"An unexpected error occurred: {str(e)}")
        else:
            messages.error(request, "Please fix the form errors below.")
    else:
        form = TrainerSignupForm()

    return render(request, 'trainers/signup.html', {'form': form})

def trainer_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'trainer':
            login(request, user)
            return redirect('trainer_dashboard')
        else:
            messages.error(request, 'Invalid trainer credentials')
    return render(request, 'trainers/login.html')

@login_required
def trainer_dashboard(request):
    trainer = get_object_or_404(Trainer, user=request.user)
    trainees = trainer.get_assigned_trainees()
    todays_activities = trainer.get_todays_activities()
    todays_weights = trainer.get_todays_weight_logs()
    return render(request, 'trainers/dashboard.html', {
        'trainer': trainer,
        'trainees': trainees,
        'todays_activities': todays_activities,
        'todays_weights': todays_weights,
    })

@login_required
def push_recommendation(request, trainee_id):
    trainer = get_object_or_404(Trainer, user=request.user)
    trainee = get_object_or_404(Trainee, id=trainee_id, trainer=trainer.user)

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Recommendation.objects.create(trainer=trainer, trainee=trainee, message=message)
            return redirect('trainer_dashboard')

    return render(request, 'trainers/push_recommendation.html', {
        'trainee': trainee
    })

@login_required
def workout_summary(request):
    trainer = get_object_or_404(Trainer, user=request.user)

    # Get all trainees assigned to this trainer
    trainees = trainer.get_assigned_trainees()

    # Get all activities for these trainees (not just today)
    activities = Activity.objects.filter(trainee__in=trainees)

    # Get all weight logs for these trainees (not just today)
    workouts = WeightLog.objects.filter(trainee__in=trainees)
    combined = list(sorted(zip(activities, workouts), key=lambda x: x[0].date))

    return render(request, 'trainers/workout_summary.html', {
        "combined": combined,
    })

@login_required
def view_attendance(request):
    trainer = get_object_or_404(Trainer, user=request.user)
    today = now().date()

    trainees = trainer.get_assigned_trainees()

    # Check if each trainee has an activity or weight log for today
    attendance_data = []
    for trainee in trainees:
        has_activity = Activity.objects.filter(date=today).exists()
        has_weight = WeightLog.objects.filter(date=today).exists()
        attendance_data.append({
            'trainee': trainee,
            'present': has_activity or has_weight,
        })

    return render(request, 'trainers/view_attendance.html', {
        'attendance_data': attendance_data,
        'date': today,
    })

@login_required
def workout_summary(request):
    trainer = get_object_or_404(Trainer, user=request.user)

    # Get all trainees assigned to this trainer
    trainees = trainer.get_assigned_trainees()

    # Get all activities for these trainees (not just today)
    activities = Activity.objects.filter(trainee__in=trainees)

    # Get all weight logs for these trainees (not just today)
    workouts = WeightLog.objects.filter(trainee__in=trainees)
    combined = list(sorted(zip(activities, workouts), key=lambda x: x[0].date))

    return render(request, 'trainers/workout_summary.html', {
        "combined": combined,
    })


@login_required
def delete_recommendation(request, recommendation_id):
    trainer = get_object_or_404(Trainer, user=request.user)
    recommendation = get_object_or_404(Recommendation, id=recommendation_id, trainer=trainer)

    if request.method == 'POST':
        trainee_name = recommendation.trainee.user.username
        recommendation.delete()
        messages.success(request, f"Recommendation to {trainee_name} has been deleted.")
        return redirect('view_recommendations')

    return render(request, 'trainers/delete_recommendation.html', {'recommendation': recommendation})


@login_required
def view_recommendations(request):
    trainer = get_object_or_404(Trainer, user=request.user)
    recommendations = Recommendation.objects.filter(trainer=trainer).order_by('-created_at')
    return render(request, 'trainers/view_recommendations.html', {'recommendations': recommendations})