from dog.models import *
from schedule.models import *
import datetime

def basic_solution():
    Schedule.objects.all().delete()
    
    w = Schedule.objects.create(start = datetime.date.today() + datetime.timedelta(days = 1), 
                                end = datetime.date.today() + datetime.timedelta(days = 8))
    w.dogs=Dog.objects.all()
    w.walkers=Walker.objects.all()
    
    w.solve()
    w.choose_solution()
