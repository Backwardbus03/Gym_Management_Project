from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django import forms
from users.models import CustomUser
from trainers.models import Recommendation
from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import Trainee, Activity, WorkoutTarget, WeightLog, CalorieLog
from django.contrib.auth.decorators import login_required
from datetime import timedelta, date
from .forms import *
from django.utils.timezone import now


class TraineeSignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    trainer = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(role='trainer'),
        required=False,
        empty_label='No trainer'
    )


def trainee_signup(request):
    if request.method == 'POST':
        form = TraineeSignupForm(request.POST)
        if form.is_valid():
            try:
                # 1. Create the CustomUser with role='trainee'
                user = CustomUser.objects.create_user(
                    username=form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'],
                    role='trainee'
                )

                # 2. Create Trainee Profile
                trainee = Trainee(
                    user=user,
                    trainer=form.cleaned_data['trainer']
                )

                # 3. Run model validation (custom clean methods)
                trainee.full_clean()
                trainee.save()

                # 4. Log the user in and redirect
                login(request, user)
                return redirect('trainee_dashboard')

            except ValidationError as ve:
                user.delete()  # rollback if the profile fails
                form.add_error(None, ve.message_dict)

            except Exception as e:
                form.add_error(None, f"An unexpected error occurred: {str(e)}")
        else:
            messages.error(request, "Please fix the form errors below.")
    else:
        form = TraineeSignupForm()

    return render(request, 'trainees/signup.html', {'form': form})

def trainee_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.role == 'trainee':
            login(request, user)
            return redirect('trainee_dashboard')
        else:
            messages.error(request, 'Invalid trainee credentials')
    return render(request, 'trainees/login.html')

def generate_recommendation(trainee):
    last_activity = Activity.objects.filter(trainee=trainee).order_by('-date').first()
    if not last_activity:
        return "Start light today with some cardio!"
    if last_activity.name.lower() == 'treadmill' and last_activity.duration_minutes > 30:
        return "Go easy today. Try yoga or stretching."
    elif last_activity.name.lower() == 'weightlifting':
        return "Consider a light cardio session today."
    return "Keep up the good work!"

@login_required
def trainee_dashboard(request):
    trainee = request.user.trainee_profile
    today = now().date()
    one_week_ago = today - timedelta(days=7)

    activities = Activity.objects.filter(trainee=trainee, date__gte=one_week_ago)
    weight_logs = WeightLog.objects.filter(trainee=trainee).order_by('-date')[:5]

    weekly_minutes = sum(a.duration_minutes for a in activities)
    weekly_calories = sum(a.calories_burned for a in activities)

    # Trainer recommendation for today
    today_recommendation = Recommendation.objects.filter(
        trainee=trainee,
        created_at__date=today
    ).order_by('-created_at').first()

    if today_recommendation:
        recommendation = today_recommendation.message
    else:
        recommendation = generate_recommendation(trainee)

    context = {
        'weekly_minutes': weekly_minutes,
        'weekly_calories': weekly_calories,
        'weight_logs': weight_logs,
        'recommendation': recommendation,
    }

    return render(request, 'trainees/dashboard.html', context)

@login_required
def log_activity(request):
    trainee = request.user.trainee_profile
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.trainee = trainee
            activity.save()
            return redirect('trainee_dashboard')
    else:
        form = ActivityForm()
    return render(request, 'trainees/log_activity.html', {'form': form})

@login_required
def log_weight(request):
    trainee = request.user.trainee_profile
    if request.method == 'POST':
        form = WeightLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.trainee = trainee
            log.save()
            return redirect('trainee_dashboard')
    else:
        form = WeightLogForm()
    return render(request, 'trainees/log_weight.html', {'form': form})


@login_required
def view_workout_target(request):
    trainee = get_object_or_404(Trainee, user=request.user)
    target = WorkoutTarget.objects.filter(trainee=trainee).first()
    return render(request, 'trainees/workout_target.html', {
        'target': target
    })


@login_required
def create_workout_target(request):
    trainee = get_object_or_404(Trainee, user=request.user)

    # Check if target already exists
    if WorkoutTarget.objects.filter(trainee=trainee).exists():
        return redirect('view_workout_target')

    if request.method == 'POST':
        weekly_minutes = request.POST.get('weekly_minutes')
        target_calories = request.POST.get('target_calories')
        target_weight = request.POST.get('target_weight') or None

        WorkoutTarget.objects.create(
            trainee=trainee,
            weekly_minutes=weekly_minutes,
            target_calories=target_calories,
            target_weight=target_weight
        )
        return redirect('view_workout_target')

    return render(request, 'trainees/create_workout_target.html')


@login_required
def update_workout_target(request):
    trainee = get_object_or_404(Trainee, user=request.user)
    target = get_object_or_404(WorkoutTarget, trainee=trainee)

    if request.method == 'POST':
        target.weekly_minutes = request.POST.get('weekly_minutes')
        target.target_calories = request.POST.get('target_calories')
        target.target_weight = request.POST.get('target_weight') or None
        target.save()
        return redirect('view_workout_target')

    return render(request, 'trainees/update_workout_target.html', {
        'target': target
    })


@login_required
def view_calorie_log(request):
    trainee = get_object_or_404(Trainee, user=request.user)
    calorie_logs = CalorieLog.objects.filter(trainee=trainee).order_by('-date')
    calorie_difference = [log.calories_consumed - log.calories_burned for log in calorie_logs]
    calorie_logs = zip(calorie_logs, calorie_difference)
    return render(request, 'trainees/calorie_log.html', {
        'calorie_logs': calorie_logs,
    })


@login_required
def log_calories(request):
    trainee = get_object_or_404(Trainee, user=request.user)

    if request.method == 'POST':
        calories_burned = request.POST.get('calories_burned')
        calories_consumed = request.POST.get('calories_consumed')

        CalorieLog.objects.create(
            trainee=trainee,
            calories_burned=calories_burned,
            calories_consumed=calories_consumed
        )
        return redirect('view_calorie_log')

    return render(request, 'trainees/log_calories.html')


@login_required
def delete_activity(request, activity_id):
    trainee = request.user.trainee_profile
    activity = get_object_or_404(Activity, id=activity_id, trainee=trainee)

    if request.method == 'POST':
        activity_name = activity.name
        activity.delete()
        messages.success(request, f"Activity '{activity_name}' has been deleted.")
        return redirect('view_activities')

    return render(request, 'trainees/delete_activity.html', {'activity': activity})


@login_required
def delete_weight_log(request, log_id):
    trainee = request.user.trainee_profile
    weight_log = get_object_or_404(WeightLog, id=log_id, trainee=trainee)

    if request.method == 'POST':
        date = weight_log.date
        weight_log.delete()
        messages.success(request, f"Weight log from {date} has been deleted.")
        return redirect('view_weight_logs')

    return render(request, 'trainees/delete_weight_log.html', {'weight_log': weight_log})


@login_required
def delete_calorie_log(request, log_id):
    trainee = request.user.trainee_profile
    calorie_log = get_object_or_404(CalorieLog, id=log_id, trainee=trainee)

    if request.method == 'POST':
        date = calorie_log.date
        calorie_log.delete()
        messages.success(request, f"Calorie log from {date} has been deleted.")
        return redirect('view_calorie_log')

    return render(request, 'trainees/delete_calorie_log.html', {'calorie_log': calorie_log})


# Add view for activities list
@login_required
def view_activities(request):
    trainee = request.user.trainee_profile
    activities = Activity.objects.filter(trainee=trainee).order_by('-date')
    return render(request, 'trainees/view_activities.html', {'activities': activities})


# Add view for weight logs list
@login_required
def view_weight_logs(request):
    trainee = request.user.trainee_profile
    weight_logs = WeightLog.objects.filter(trainee=trainee).order_by('-date')
    return render(request, 'trainees/view_weight_logs.html', {'weight_logs': weight_logs})