from django.db import models
from django.contrib.auth.models import User, Group, Permission

## ===== User =====
# class User(models.Model):
#     username = models.CharField(max_length=20)
#     nickname = models.CharField(max_length=20)
#     password = models.CharField(max_length=20)
#     privilege = models.IntegerField(default=2) # 0 - superuser, 1 - admin
# 
#     def __str__(self):
#         return "User: {} [pk={}]".format(self.username, self.pk)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    last_activity = models.DateTimeField(auto_now_add=True)
    userrank = models.CharField(max_length=30, default="Junior Member")
    last_posttime = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(max_length=1000, blank=True)

    def __unicode__(self):
        return self.user.username

#     def get_total_posts(self):
#         return self.user.post_set.count()
# 
#     def get_absolute_url(self):
#         return self.user.get_absolute_url()
