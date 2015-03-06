import django
from django.contrib.auth.models import User
from qishi.models import Category, Forum, Topic, Post

 
c1 = Category.objects.create(name="QishiClub",description = "club")
c2 = Category.objects.create(name="Q&A",description = "discussion")

f1 = Forum.objects.create(name="Premium Club",slug="PremiumClub", description = "for premium members",
        category = c1)
 


 
forum = Forum(name="Career Club", slug="CareerClub",description = "for career excellence", category = c1)
forum.save()

forum = Forum(name="Machine Learning Group",slug="MLGroup", description = "study group", category = c2)
forum.save()


Category.objects.all()
c1.forum_set.all()



blogs = Topic.objects.filter(topic_type__slug="blog")
 
 