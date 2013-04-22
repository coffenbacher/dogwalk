import datetime
from dog.helpers import basic_solution
from schedule.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
import json

@login_required
def home(request):
    
    if request.method == 'POST' or not Schedule.objects.all():
        basic_solution()

    w = Schedule.objects.all()[0] 
    return render_to_response('home.html', {'w': w})
