import django
from django.contrib.auth.models import User
from qishi.models import Category, Forum, Topic, Post

 
c1 = Category.objects.create(name="QishiClub")
c2 = Category.objects.create(name="Q&A",description = "discussion")

f1 = Forum.objects.create(name="Premium Club", description = "for premium members",
        category = c1)
 


 
forum = Forum(name="Career Club", description = "for career excellence", category = c1)
forum.save()

Category.objects.all()
c1.forum_set.all()



blogs = Topic.objects.filter(topic_type__slug="blog")
 
 