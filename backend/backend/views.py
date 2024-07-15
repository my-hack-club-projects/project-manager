from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

def home(request, path=None):
    if request.user.is_authenticated:
        return redirect('/projects')
    
    return render(request, 'index.html')

@login_required
def projects(request, path=None):
    return render(request, 'index.html')

def anyother(request, path=None):
    return render(request, 'index.html')