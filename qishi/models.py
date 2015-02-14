from django.db import models

# ===== User =====
class User(models.Model):
    username = models.CharField(max_length=20)
    nickname = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    privilege = models.IntegerField(default=2) # 0 - superuser, 1 - admin

    def __str__(self):
        return "User: {} [pk={}]".format(self.username, self.pk)
