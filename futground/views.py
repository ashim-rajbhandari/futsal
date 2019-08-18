from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from futground.models import Ground,Reservation,Rating
from .forms import UserReservationForm,RatingForm
from django.contrib.auth.models import User
from django.contrib import messages
from datetime import date
from django.utils.dateparse import parse_date
from datetime import timedelta
from django.db.models import Q
import random
import math


def home(request):
    return render(request, 'futground/home.html')


def evaluate_cosine_similarity(user,similar_user):
    numerator = 0
    user_square_sum = 0
    similar_user_square_sum = 0

    for i in range(len(user)-1):
        numerator = numerator + (user[i]*similar_user[i])
        user_square_sum = user_square_sum + (user[i]*user[i])
        similar_user_square_sum = similar_user_square_sum + (user[i]*user[i])

    denominator = math.sqrt(user_square_sum) + math.sqrt(similar_user_square_sum)
    similarity = numerator/denominator
    return similarity


def predict_user_item_rating(user,similar_user,cosine_similarity):
    denominator = 0
    predictate_rating = []

    similar_user_average = []
    user_average = 0

    for i in range(len(cosine_similarity)):
        denominator = denominator + cosine_similarity[i]

    for i in range(len(similar_user)):
        average = 0;
        total = 0;
        for j in range(len(similar_user[0])):
            total = total + similar_user[i][j]
        average = total/len(similar_user[0])
        similar_user_average.append(average)

    total = 0
    for i in range(len(user)):
        total = total + user[i]
    user_average  = total/len(user)

    for j in range(len(similar_user[0])):
        numerator = 0
        for i in range(len(similar_user)):
            numerator = numerator + ((similar_user[i][j]-similar_user_average[i])*cosine_similarity[i])
        predict = user_average + (numerator/denominator)
        predictate_rating.append(predict)

    return predictate_rating

def removingDuplicates(listOfElements):
    uniqueList = []

    for elem in listOfElements:
        if elem not in uniqueList:
            uniqueList.append(elem)

    return uniqueList

def similar_ground(user_id):
    user_rated_ground = []
    similar_rating_user_id = []
    similar_user_rated_grounds = []
    rating = Rating.objects.filter(user=user_id)

    #get the grounds rated by active user
    for rating in rating:
        user_rated_ground.append(rating.ground)

    #get the similar users who rated the grounds rated by active user
    similar_rating = Rating.objects.filter(ground__in=user_rated_ground).order_by('user_id').exclude(user_id=user_id)

    #prepare the list of similar rating users and the grounds they rated
    for s in similar_rating:
        similar_rating_user_id.append(s.user_id)

        for h in Rating.objects.filter(user_id=s.user_id):
            similar_user_rated_grounds.append(h.ground_id)

    #print(similar_user_rated_grounds)
    # removing duplicates
    if similar_rating_user_id and similar_user_rated_grounds:
         similar_rating_user_id = removingDuplicates(similar_rating_user_id)
         similar_user_rated_grounds = removingDuplicates(similar_user_rated_grounds)

    similar_rating_user_id.sort()
    similar_user_rated_grounds.sort()

    #create user-item matrix for both active user and similar users
    similar_user =  [[0] * len(similar_user_rated_grounds) for i in range(len(similar_rating_user_id))]
    user = []

    for i,similar_user_id in enumerate(similar_rating_user_id):
        for j,ground_id in enumerate(similar_user_rated_grounds):
            if Rating.objects.filter(user_id=similar_user_id,ground_id=ground_id).exists():
                r = Rating.objects.values('rate').get(user_id=similar_user_id,ground_id=ground_id)
                rate1 = r['rate']
            else:
               rate1 = 0
            similar_user[i][j] = rate1


    for j in similar_user_rated_grounds:
        if Rating.objects.filter(user_id=user_id, ground_id=j).exists():
            r = Rating.objects.values('rate').get(user_id=user_id, ground_id=j)
            rate1 = r['rate']
        else:
            rate1 = 0
        user.append(rate1)

    #calculating similarity through cosine similarity
    cosine_similarity = []

    for i in range(len(similar_rating_user_id)):
        similarity = evaluate_cosine_similarity(user,similar_user[i])
        cosine_similarity.append(similarity)

    ground = []

    if cosine_similarity:
        #predicting the rating for the each item of active user
        predictate_rating = predict_user_item_rating(user,similar_user,cosine_similarity)

        #now finding the top predictate ground rating
        predictate_similar_ground = []
        grounds = []
        for j, ground_id in enumerate(similar_user_rated_grounds):
            predictate_similar_ground.append((ground_id,predictate_rating[j]))
        predictate_similar_ground.sort(key=lambda x  : x[1],reverse=True)

        for p in predictate_similar_ground:
            grounds.append(p[0])

        for h in grounds:
            ground.append( Ground.objects.get(id=h))

    return ground[:10]

@login_required()
def recommend(request):
    if Rating.objects.filter(user=request.user.id).exists():
      similar = similar_ground(request.user.id)
      context = {'ground': similar}
    else:
        messages.info(request, f'cold start,need more ratings')
        return redirect('futground:fut-list')

    return render(request, 'futground/recommendation.html',context)

def list(request):
    all_grounds = Ground.objects.all()


    rating = Rating.objects.values_list('avg_rating','ground').order_by('-avg_rating').distinct()[:5]
    ground = []
    for rating in rating:
        ground.append(int(rating[1]))

    all_ratings = Ground.objects.filter(id__in=ground)

    #similar = similar_ground(request.user.id)
    #print(request.user.id)


    context = {'all_grounds': all_grounds,'all_ratings':all_ratings}
    return render(request, 'futground/list.html', context)


@login_required()
def detail(request, ground_id):
    ground = Ground.objects.get(pk=ground_id)
    user = request.user.id

    if request.method == 'POST' and 'res_btn' in request.POST:
      form1 = UserReservationForm(request.POST)
      gd = request.POST.get('ground')
      st = request.POST.get('starting_time')
      et = request.POST.get('ending_time')
      rd = request.POST.get('reserved_date')
      res = Reservation()
      r = parse_date(rd)

      print(st)
      print(et)
      print(rd)
      print(type(r))


      if r == None or r < date.today() or r > date.today() + timedelta(days=7) or st > et or st < '10:00:00' or et > '18:00:00':
        print("sdas")
        messages.success(request,f'time format mistake')


      elif Reservation.objects.filter(ground=gd,starting_time = st,reserved_date=rd,ending_time = et).exists():
           messages.success(request, f'already reserved time slot')
           #return redirect('futground:fut-detail')

      else:

        if form1.is_valid():
            res.ground = Ground.objects.get(pk=gd)
            res.starting_time = st
            res.ending_time = et
            res.reserved_date = r
            res.user = request.user.id

            res.save()
            messages.success(request, f'successfully reserved')
            return redirect('futground:fut-rate',ground_id)


        else:
         print("form invalid")
         print(form1.errors)




    else:
       form1 = UserReservationForm(initial={'ground': ground_id})

    return render(request,'futground/detail.html',{'ground':ground,'form1':form1,'user_id' : request.user.id})

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

@login_required()
def search(request):


    if request.method == 'POST':
      s1 = request.POST.get('srch')
      s = Ground.objects.filter(
                                Q(name__istartswith=s1)
                                )


    return render(request,'futground/search.html',{'s':s})


@login_required()
def rate(request,ground_id):
    ground = Ground.objects.get(pk=ground_id)
    user = request.user.id
    form = RatingForm(request.POST)
    if request.method == 'POST' and 'rt_btn' in request.POST:
        form = RatingForm(request.POST)
        r = Rating()
        rt = request.POST.get('rate')
        rtu = request.POST.get('user')
        rtg = request.POST.get('ground')

        if Rating.objects.filter(user_id=user, ground_id=ground).exists():
            Rating.objects.filter(user_id=user, ground_id=ground).update(rate=rt)
            messages.success(request, f'updated rate')
            return redirect('futground:fut-list')



        elif form.is_valid():
            r.rate = rt
            r.user_id = rtu
            r.ground_id = rtg
            r.save()
            messages.success(request, f'rated')
            return redirect('futground:fut-list')
    else:
      form = RatingForm(initial={'ground': ground_id,'user':request.user.id})

    return render(request, 'futground/rate.html', {'ground': ground, 'form': form, 'user': request.user.id})

#def khalti(request,ground_id):
       #return render(request, 'futground/khalti.html')

