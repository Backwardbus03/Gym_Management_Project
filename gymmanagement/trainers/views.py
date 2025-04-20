from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def dashboard(request):
    if request.user.role != 'trainer':
        return HttpResponseForbidden("You are not a trainer.")
    return render(request, 'trainers.html')
