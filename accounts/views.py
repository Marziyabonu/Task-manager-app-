from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import SimplestUserCreationForm as RegisterForm
from django.contrib.auth.decorators import login_required
from tasks.models import Task

def register(request):
    if request.user.is_authenticated:
        return redirect('task_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user) 
                return redirect('task_list')
            except IntegrityError:
                form.add_error('username', "❌ Bu foydalanuvchi nomi allaqachon band qilingan. Boshqa nom tanlang.")
                
    else:
        form = RegisterForm()
        
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)

def login_view(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['username'],
            password=request.POST['password']
        )
        if user:
            login(request, user)
            return redirect('task_list')

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user_tasks = Task.objects.filter(user=request.user)
    
    total_tasks = user_tasks.count()
    completed_tasks = user_tasks.filter(status='done').count()
    
    if total_tasks > 0:
        completion_percentage = int((completed_tasks / total_tasks) * 100)
    else:
        completion_percentage = 0
        
    context = {
        'user': request.user,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_percentage': completion_percentage,
    }
    
    return render(request, 'accounts/profile.html', context)