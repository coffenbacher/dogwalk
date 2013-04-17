from dog.models import *
from graph.models import *
from schedule.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    
    if request.method == 'POST':
        Week.objects.all().delete()
        
        w = Week.objects.create()
        w.dogs=Dog.objects.all()
        w.walkers=Walker.objects.all()
        
        w.solve()
        w.choose_solution()

    ws = Week.objects.all()

    return render_to_response('home.html', {'ws': ws})


