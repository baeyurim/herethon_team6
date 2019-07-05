from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Trip, Comment
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.storage import FileSystemStorage
from .forms import TripForm, CommentForm
from django.contrib.auth.models import User
from django.contrib import auth

def home(request):
 
    if request.method == 'GET':
        trip=Trip.objects.all()
        trip_list = Trip.objects.all()
    
        sel_budget = request.GET.get('sel_budget', '')
        sel_place = request.GET.get('sel_place','')
        sel_transportation = request.GET.get('sel_transportation','')
        if sel_budget and sel_place and sel_transportation:
            trip_list = trip_list.filter(budget__icontains=sel_budget)
            trip_list = trip_list.filter(place__icontains=sel_place)
            trip_list = trip_list.filter(transportation__icontains=sel_transportation)

        paginator = Paginator(trip_list, 4)
        page = request.GET.get('page')

    else:

        trip=Trip.objects.all()
        trip_list = Trip.objects.all()
        paginator = Paginator(trip_list, 4)
        page = request.GET.get('page')
        
    try:
       posts = paginator.get_page(page)
    except PageNotAnInteger:            
        posts = paginator.get_page(1)
    except EmptyPage:
        posts = paginator.get_page(paginator.num_pages)
    return render(request, 'home.html', {'trip':trip, 'posts':posts})

    # trip=Trip.objects.all()
    # trip_list = Trip.objects.all()
    # paginator = Paginator(trip_list, 4)
    # page = request.GET.get('page')
    # try:
    #     posts = paginator.get_page(page)
    # except PageNotAnInteger:            
    #     posts = paginator.get_page(1)
    # except EmptyPage:
    #     posts = paginator.get_page(paginator.num_pages)
    # return render(request, 'home.html', {'trip':trip, 'posts':posts})

def promotion(request):
    return render(request, 'promotion.html')

def detail(request, trip_id):
    trip=get_object_or_404(Trip, pk=trip_id)

    return render(request, 'detail.html', {'trip':trip})

def new(request):
    
    if request.method == 'GET':
        form = TripForm()
        return render(request, 'new.html', {'form':form})

    else:
        trip = Trip()
        form = TripForm(request.POST)
        if form.is_valid():
            trip = form.save(commit=False)
           
            images = request.FILES['image']
            im = FileSystemStorage()
            trip.image = im.save(images.name, images)
            
            trip.writer = request.user

            trip.save()
        return redirect('/')



def detail(request, trip_id):
    trip=get_object_or_404(Trip, pk=trip_id)

    return render(request, 'detail.html', {'trip':trip})

def edit(request, trip_id):

    trip = get_object_or_404(Trip, pk=trip_id)

    if request.method == 'GET':
        form = TripForm(instance=trip)
        return render(request, 'edit.html', {'form':form})
    
    else:        
        
        form = TripForm(request.POST, instance = trip)
        if form.is_valid():
            trip = form.save(commit=False)
            
            images = request.FILES['image']
            im = FileSystemStorage()
            trip.image = im.save(images.name, images)
            
            trip.date = timezone.now() 

            trip.save()
    
        return redirect('/' + str(trip_id))


def delete(request, trip_id):
    trip = get_object_or_404(Trip, pk=trip_id)
    trip.delete()

    return redirect('/')


def signup(request):
    if request.method == 'POST':

        if request.POST['username'] == '' or request.POST['password'] == '':
            return render(request, 'signup.html', {'error':'아이디 비밀번호를 입력하세요'})
        
        if request.POST['password'] != request.POST['con_password']:
            return render(request, 'signup.html', {'error':'비밀번호 불일치'})

        try :
            user = User.objects.get(username = request.POST['username'])
            return render(request, 'signup.html', {'error':'이미 존재하는 이름'})
        except User.DoesNotExist:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
            auth.login(request, user)

            return redirect('/')


    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        pw = request.POST['password']

        user = auth.authenticate(request, username = username, password = pw)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error':'아이디, 비밀번호 확인'})

    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

     
def comment_create(request, trip_id):

        if request.method == 'POST':
                trip = get_object_or_404(Trip, pk=trip_id)
                form = CommentForm(request.POST)
                
                if form.is_valid():
                        comment = form.save(commit=False)
                        comment.trip = trip
                        comment.com_writer = request.user

                        comment.save()
                return redirect('/' + str(trip.id))
        else:
                form=CommentForm()
                return render(request, 'detail.html', {'form':form})


def comment_delete(request, trip_id, comment_id):
        trip = get_object_or_404(Trip, pk=trip_id)
        comment = get_object_or_404(Comment, pk=comment_id)

        comment.delete()

        return redirect('/' + str(trip.id))


