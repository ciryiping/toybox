import django
from qishi.models import User

User.objects.all().delete()

u = User(username="su",
         password="123456",
         nickname="Super User",
         privilege=0)
u.save()
print("Add Super User\n")


u = User(username="admin",
         password="123456",
         nickname="Administrator",
         privilege=1)
u.save()
print("Add Administrator\n")


for i in range(10):
    u = User(username="user{}".format(i),
             password="pwd{}".format(i),
             nickname="nick{}".format(i))
    u.save()
    print("Add User {}".format(i))
