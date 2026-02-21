from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)

    search = request.GET.get('search')
    if search:
        tasks = tasks.filter(title__icontains=search) 

    status = request.GET.get('status')
    if status:
        tasks = tasks.filter(status=status)

    priority = request.GET.get('priority')
    if priority:
        tasks = tasks.filter(priority=priority)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            title=request.POST['title'],
            description=request.POST['description'],
            priority=request.POST['priority'],
            deadline=request.POST['deadline'],
        )
        return redirect('task_list')
    return render(request, 'tasks/task_create.html')

@login_required
def task_update(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.priority = request.POST['priority']
        task.deadline = request.POST['deadline']
        task.status = request.POST['status']
        task.save()
        return redirect('task_list')

    return render(request, 'tasks/task_update.html', {'task': task})

@login_required
def task_delete(request, id):
    """Taskni o'chirish (faqat POST orqali ruxsat beriladi)"""
    task = get_object_or_404(Task, id=id, user=request.user)

    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    
    return redirect('task_list')
