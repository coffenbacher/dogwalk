import datetime
from dog.models import *
from graph.models import *
from schedule.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import json

@login_required
def home(request):
    
    if request.method == 'POST' or not Schedule.objects.all():
        Schedule.objects.all().delete()
        
        w = Schedule.objects.create(start = datetime.date.today() + datetime.timedelta(days=1))
        w.dogs=Dog.objects.all()
        w.walkers=Walker.objects.all()
        
        w.solve()
        w.choose_solution()

    w = Schedule.objects.all()[0] 
    return render_to_response('home.html', {'w': w})
