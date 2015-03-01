#import django
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

#User.objects.all().delete()

user = User.objects.create_user( username="superuser",   password="123456" )
user.is_staff = True
user.save
user = User.objects.create_user( username="test1",   password="123123")
user = User.objects.create_user( username="test2",   password="123123")
user = authenticate( username="test1",password="123123")

 
 