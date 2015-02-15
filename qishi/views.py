from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.contrib.auth.models import User

#from qishi.models import User


def getUserInfo(request):
    """Parse User Info
    If the user has logged in, the function will return a dictionary with two entries:
      memberId, username 
    If the user's login is unsuccessfuld
    """
    params = {
      "memberId"  : request.session.get("memberId", False),    
      "username"  : request.session.get("username", False),
#      "nickname"  : request.session.get("nickname", False),
#      "privilege" : request.session.get("privilege", 99),
    }
    
    if params['memberId']  :
        pass
    else:
        params = {}

    params["base_url"] = settings.BASE_URL
    return params
           

def index(request):
    params = getUserInfo(request)
    return render(request, "qishi/index.html", params)


def login(request):

    # Check if user is already logged in
    if request.session.get("memberId", False)  :
        return index(request)

    params = {'login_failed' : False}
    
    # If username is in the post data
    if request.POST.get('username', False):
        try:
            u = User.objects.get(username=request.POST['username'])
        except:
            pass
        else:
            if u.password == request.POST['password']:
                request.session['memberId']   = u.pk
                request.session['username']  = u.username
#                request.session['nickname']   = u.nickname
#                request.session['privilege'] = u.privilege
                return index(request)
        params['login_failed'] = True

    # display the login page
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
            u = User(username = username,
                     password = password)
            u.save()
            return login(request)
        except:
            params['failed'] = "Cannot register (database error)."
        
    # display the register page
    return render(request, 'qishi/register.html', params)



def logoff(request):
    try:
        del request.session['memberId']
    except KeyError:
        pass
    try:
        del request.session['username']
    except KeyError:
        pass

#    try:
#        del request.session['nickname']
#    except KeyError:
#        pass
        
#    request.session['priviledge'] = 99
    return index(request)


def admin(request):

    # First check if user is already logged in
    if request.session.get("memberId", False) and \
       request.session.get("username", False):
        return render(request, "qishi/admin_refuse.html", {})

    # Load User info
    try:
        u = User.objects.get(pk=request.session.get("memberId"))
    except:
        return render(request, "qishi/admin_refuse.html", {})

    if not u.is_staff:
        return render(request, "qishi/admin_refuse.html", {})

    # List all users    
    user_list = User.objects.all()

    params = { 'user_list': user_list }
    return render(request, "qishi/admin.html", params)



def page_not_found(request):
    return HttpResponse("Qishi 404: Page Not Found.")
