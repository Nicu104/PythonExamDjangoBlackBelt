from django.db import models
from django.contrib import messages
from django.contrib.messages import get_messages
from passlib.hash import pbkdf2_sha256
from datetime import datetime
from dateutil import parser


class UserManager(models.Manager):
    
    def validateUser(self, request):
        name = request.POST['name']
        username = request.POST['user_name']
        paswd = request.POST['password']
        paswd_conf = request.POST['password_conf']
        if len(name) < 3:
            messages.add_message(request, messages.ERROR, "Your name should be at least 3 char long")
        
        if len(username) < 3:
            messages.add_message(request, messages.ERROR, "User name should be at least 3 chars long")

        if len(paswd) < 8 or paswd != paswd_conf:
            messages.add_message(request, messages.ERROR, 'Password does not match or is shorter than 8 characters')

        if len(Users.objects.filter(user_name = username)) != 0:
            messages.add_message(request, messages.ERROR, "A user with this username exists already, please contact the admin")

        if len(get_messages(request)) > 0:
            return False
        else:
            password = paswd
            enc_pass = pbkdf2_sha256.encrypt(paswd, rounds = 12000, salt_size = 32)

            Users.objects.create(
                name = name,
                user_name = username,
                password = enc_pass
            )
            return True
    

    def validateTrip(self, request):
        dest = request.POST['destination']
        desc = request.POST['description']
        # dt = parser.parse("Aug 28 1999 12:00AM")
        travelDate = parser.parse(request.POST['travel_start'])
        travelEnd = parser.parse(request.POST['travel_end'])

        if len(dest) < 1:
            messages.add_message(request, messages.ERROR, "Destination cannot be empty")
        if len(desc) < 1:
            messages.add_message(request, messages.ERROR, "Description cannot be empty")
        if travelDate < datetime.now():
            messages.add_message(request, messages.ERROR, "Travel start nate should be in future")
        if travelDate > travelEnd:
            messages.add_message(request, messages.ERROR, "Travel end date  should be  greater than start date")
        
        if len(get_messages(request)) > 0:
            return False
        else:
            Travels.objects.create(
                destination = dest,
                description = desc,
                travel_start = travelDate,
                travel_end = travelEnd,
                user_id = request.session['id'],
            )
            return True


class Users(models.Model):
    name = models.CharField(max_length = 255)
    user_name = models.CharField(max_length = 255)
    password = models.TextField()
    objects = UserManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)


class Travels(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name = 'travels')
    joined_users = models.ManyToManyField(Users, related_name = 'travel_joined')
    travel_start = models.DateTimeField()
    travel_end = models.DateTimeField() 
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()