from django.shortcuts import render, redirect, reverse, HttpResponse
from .models import *
from passlib.hash import pbkdf2_sha256

# Create your views here.

def index(request):
    if not 'id' in request.session:
        return render(request, 'mainapp/index.html')
    else:
        return redirect(reverse('users:travel'))


#TODO display all trips on screen
#planned by user and other that can be joined
def travel(request):
    otherTrips = []
    if not "id" in request.session:
        return render(request, 'mainapp/nologin.html')
    else:
        userID = request.session['id']
        user = Users.objects.get(id = userID)
        
        tripsInitiated = Travels.objects.filter(user_id = userID) | Travels.objects.filter(joined_users = user)

        # otherTrips = Travels.objects.exclude(user = userID) | Travels.objects.filter(joined_users = user)

        allT = Travels.objects.all()
        for trip in allT:
            if not trip in tripsInitiated :
                otherTrips.append(trip)
      
        context ={
            'trips' : tripsInitiated,
            'othertrips' : otherTrips,
            'user' : user
        }
        return render(request, 'mainapp/travels.html', context)

#TODO takes an id of the destination and shows all the info about 
# prints all other users that joined this trip
def destination(request, id):
    trip = Travels.objects.get(id = id)
    users = Users.objects.filter(travel_joined = trip)
    return render(request, 'mainapp/tripinfo.html', {
        'trip' : trip,
        'users' : users
        })


#TODO display a form to create another trip
def addtrip(request):
    return render(request, 'mainapp/addtrip.html')


#TODO this method will take the POST data and add a new travel to db
# no empty entries travel dates should be future-dated
#TRaveel to  should not be before the travel dare from
# once added it should redirect user to the dashboard
def createtrip(request):
    travel = Travels.objects.validateTrip(request)
    if travel:
        return redirect(reverse('users:travel'))
    else:
        return redirect(reverse('users:addtrip'))

#TODO on href click add this trip to existing ones
def jointrip(request, id):
    userID = request.session['id']
    user = Users.objects.get(id = userID)
    trip = Travels.objects.get(id = id)
    user.travel_joined.add(trip)
    # print(user, trip)
    return redirect(reverse('users:travel'))

def logout(request):
    request.session.flush()
    return redirect(reverse('users:home'))

#TODO this method will add a new user just after all vaidations are done
# name and username should be at least 3 chars 
# password should be at least 8 chars long
#redirect to dahsboard
def createuser(request):
    if Users.objects.validateUser(request):
        user = Users.objects.last()
        request.session['id'] = user.id
        return redirect(reverse('users:travel'))
    else:
        return redirect(reverse('users:home'))


#TODO this will log in the user
# onced logged will take to dashboard
def login(request):
    try:
        username = request.POST['user_name']
        password = request.POST['password']
        user = Users.objects.get(user_name = username)
        if pbkdf2_sha256.verify(password, user.password):
            request.session['id'] = user.id
            return redirect(reverse('users:travel'))
        else:
            messages.add_message(request, messages.ERROR, "Wrong password")
            return redirect(reverse('users:home'))                 
    except:
            messages.add_message(request, messages.ERROR, "No user found tith this credentials")
            return redirect(reverse('users:home'))     
    