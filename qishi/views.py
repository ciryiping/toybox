from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from qishi.models import Topic, Forum, Post

#to be added later
#from forms import EditPostForm, NewPostForm, ForumForm
#import settings as lbf_settings

           

def index(request):
    ctx = {}
    ctx['topics'] = Topic.objects.all()  #.order_by('-last_reply_on')[:20]
    ctx['categories'] = Category.objects.all()
    return render(request, "qishi/index.html", ctx)

def my_login(request):
    if request.user.is_authenticated():
        return index(request)
    params = {'login_failed' : False}
    
    # If username is in the post data
    if request.POST.get('username', False):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return index(request)
            else:
                # Return a 'disabled account' error message
                params['login_failed'] = True
        else:
        # Return an 'invalid login' error message.
            params['login_failed'] = True
            
    template = loader.get_template('qishi/login.html')
    context = RequestContext(request, params)
    return  HttpResponse(template.render(context))

 

def register(request):

    # Check if user is already logged in    
    if request.session.get("memberId", False) and \
       request.session.get("username", False):
        return index(request)
    
    params = {'failed': False}
    
    # If username is in the post data
    username = request.POST.get('username', False)
    if username:
        if len(username) < 4:
            params['failed'] = "User name too short."
            return render(request, 'qishi/register.html', params)

        # check if username already exists
        try:
            u = User.objects.get(username = username)
        except:
            pass
        else:
            # User already exists
            params['failed'] = "User Already Exists."
            return render(request, 'qishi/register.html', params)

        # check if password is valid
#        nickname  = request.POST.get('nickname',  False)        
        password  = request.POST.get('password',  False)
        password2 = request.POST.get('password2', False)
        if password and password2 and password == password2:
            pass
        else:
            params['failed'] = "Invalid Password."
            return render(request, 'qishi/register.html', params)

        try:
            User.objects.create_user( username=username,   password=password)  
            return my_login(request)
        except:
            params['failed'] = "Cannot register (database error)."
        
    # display the register page
    return render(request, 'qishi/register.html', params)



def logoff(request):
    logout(request)
    return index(request)


def admin(request):
    # First check if user is already logged in
    if not request.user.is_authenticated():
        return render(request, "qishi/admin_refuse.html", {})
    if reqeust.user.is_staff:
        return render(request, "qishi/admin_refuse.html", {})
        
     # List all users    
    user_list = User.objects.all()

    params = { 'user_list': user_list }
    return render(request, "qishi/admin.html", params)

 





def page_not_found(request):
    return HttpResponse("Qishi 404: Page Not Found.")
