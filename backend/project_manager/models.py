from django.db import models
from django.conf import settings
from django.utils import timezone

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    locked = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Project(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=2000, default="")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class TaskContainer(models.Model):
    title = models.CharField(max_length=64)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=200)
    task_container = models.ForeignKey(TaskContainer, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Session(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=60)  # in minutes
    active = models.BooleanField(default=True)
    goal = models.TextField(default="No goal", max_length=100)
    tasks = models.ManyToManyField(Task)

    def __str__(self):
        return f"Session for {self.project.name} at {self.start_time}"
    
    def update_active_status(self):
        # if the session has been active for longer than its duration, set it to inactive
        if (self.start_time - timezone.now()).seconds > self.duration * 60:
            self.active = False
            self.save()

class Note(models.Model):
    # notes are like discord messages. they are sent in sessions and can only be sent when a session is active
    # they serve the purpose of having a place to write down your thoughts or communicate with collaborators (if any)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # the user who sent the note
    content = models.TextField(max_length=300)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note by {self.user.username} in session for {self.session.project.name}"