from django.contrib import admin

#from django.contrib.auth.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    field = ['username',   'password' ]

#admin.site.register(User, UserAdmin)    

