# Create your views here.
import json
from django.http import HttpResponse
from models import *
from django.core import serializers
from django.shortcuts import render_to_response

def show(request, pk):
    #entries = Schedule.objects.get(pk=pk).entries.all()
    entries = Schedule.objects.all()[0].entries.all()
    days = entries.dates('start', 'day')
    
    res = []
    
    p = ''
    pwalker = '' 
    for e in entries.order_by('walker', 'start'):
        if p:
            res.append({
                'walker': e.walker.name,
                'start': str(e.start.time()), 
                'end': str(e.end.time()), 
                'address': e.node.address,
                'previous_address': p})
        if pwalker != e.walker.name:
            p = ''
            pwalker = e.walker.name
        else:    
            p = e.node.address
            
    j = json.dumps(res)
    return HttpResponse(j)

def map(request, pk):
    entries = Schedule.objects.all()[0].entries.all()
    #entries = Schedule.objects.get(pk=pk).entries.all()
    
    return render_to_response('schedule/map.html', {'entries': entries})

def dogs(request, pk):
    w = Schedule.objects.all()[0]
    for d in w.main_solution.pdogs.all():
        d.validate()
    return render_to_response('schedule/dogs.html', {'w': w})
