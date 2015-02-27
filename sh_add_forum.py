import django
from django.contrib.auth.models import User
from qishi.models import Category, Forum, TopicType, Topic

category = Category(name="QishiClub")
category.save()
category = Category(name="Q&A",description = "discussion")
category.save()
Category.objects.all()
c=Category.objects.get(name="QishiClub")
forum = Forum(name="Premium Club", description = "for premium members",
        category = c)
forum.save()

forum = Forum(name="Premium Club", description = "for premium members")
forum.save()


 
 