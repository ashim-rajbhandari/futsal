from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from futground.models import Ground,Reservation
from .forms import UserReservationForm
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.db.models import Q

def home(request):
    return render(request, 'futground/home.html')

def list(request):
    all_grounds = Ground.objects.all()
    context = {'all_grounds': all_grounds}
    return render(request, 'futground/list.html', context)


@login_required()
def detail(request, ground_id):
    ground = Ground.objects.get(pk=ground_id)

    if request.method == 'POST':
      gd = request.POST.get('ground')
      st = request.POST.get('starting_time')
      et = request.POST.get('ending_time')
      rd = request.POST.get('reserved_date')
      th = request.POST.get('total_hour')
      res = Reservation()
      form = UserReservationForm(request.POST)
      r = parse_date(rd)

      if  r < date.today() or r > date.today() + timedelta(days=7) or st > et or st < '10:00:00' or et > '18:00:00':
        print("sdas")
        messages.success(request,f'time format mistake')


      elif Reservation.objects.filter(ground=gd,starting_time = st,reserved_date=rd,ending_time = et).exists():
           messages.success(request, f'already reserved time slot')
           #return redirect('futground:fut-detail')

      else:

        if form.is_valid():

            res.ground = Ground.objects.get(pk=gd)
            res.starting_time = st
            res.ending_time = et
            res.reserved_date = rd
            res.total_hour = th
            res.user = request.user.id

            res.save()
            messages.success(request, f'successfully reserved')
            return redirect('futground:fut-list')
        else:
          print("form invalid")
          print(form.errors)

    else:
       form = UserReservationForm(initial={'ground':ground_id})
       print(ground)

    return render(request,'futground/detail.html',{'ground':ground,'form':form,'user_id' : request.user.id})


def deletereservation(request,reservation_id):
    obj = Reservation.objects.get(id=reservation_id)
    print(obj)
    if request.method=="POST":
        obj.delete()
        return redirect('futground:fut-home')
    #context={
     #   "object":obj

    #}
    return render(request,'futground/reservationdelete.html')


def search(request):


    if request.method == 'POST':
      s1 = request.POST.get('srch')
      s = Ground.objects.filter(Q(name__istartswith=s1)|
                                Q(location__iexact=s1)
                                )


    return render(request,'futground/search.html',{'s':s})
