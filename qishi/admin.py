from django.contrib import admin

from qishi.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    field = ['username', 'nickname', 'password', 'priviledge']

admin.site.register(User, UserAdmin)    

