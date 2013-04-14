from dog.models import *
from schedule.models import *
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    w = Week.objects.all()
    return render_to_response('home.html', {'ws': w})

