from dog.models import *
from schedule.models import *
import datetime

def basic_solution(start = None):
    Schedule.objects.all().delete()
    
    if not start:
        start = datetime.date.today() + datetime.timedelta(days = 1)
    end = start + datetime.timedelta(days = 7)
    
    w = Schedule.objects.create(start = start, end = end)
    w.dogs=Dog.objects.all()
    w.walkers=Walker.objects.all()
    w.init()
    
    w.solve()
    w.choose_solution()
