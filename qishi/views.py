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
from qishi.models import Category, Topic, Forum, Post
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

#to be added later
from qishi.forms import EditPostForm, NewPostForm, ForumForm
#import settings as lbf_settings

           

def index(request):
    ctx = {}
    ctx['topics'] = Topic.objects.all().order_by('-last_reply_on')[:20]
    ctx['categories'] = Category.objects.all()
    #ctx['forums'] = Forum.objects.all()
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
    return HttpResponse("QishiClub 404: Page Not Found.")
 
def blogview(request):
    blogs = Topic.objects.filter(topic_type__slug="blog")
    ctx = {'blogs': blogs}
    return render(request,"qishi/blog.html", ctx)   

def forum(request, forum_slug, topic_type='', topic_type2='',
        template_name="qishi/forum.html"):
    forum = get_object_or_404(Forum, slug=forum_slug)
    topics = forum.topic_set.all()
    if topic_type and topic_type != 'good':
        topic_type2 = topic_type
        topic_type = ''
    if topic_type == 'good':
        topics = topics.filter(level__gt=30)
        #topic_type = _("Distillate District")
    if topic_type2:
        topics = topics.filter(topic_type__slug=topic_type2)
    order_by = request.GET.get('order_by', '-last_reply_on')
    topics = topics.order_by('-sticky', order_by).select_related()
    form = ForumForm(request.GET)
    ext_ctx = {'form': form, 'forum': forum, 'topics': topics,
            'topic_type': topic_type, 'topic_type2': topic_type2}
    return render(request, template_name, ext_ctx)

def topic(request, topic_id, template_name="qishi/topic.html"):
    topic = get_object_or_404(Topic, id=topic_id)
    topic.num_views += 1
    topic.save()
    posts = topic.posts
#    if lbf_settings.STICKY_TOPIC_POST:  # sticky topic post
#        posts = posts.filter(topic_post=False)
    posts = posts.order_by('created_on').select_related()
    ext_ctx = {'topic': topic, 'posts': posts}
    ext_ctx['has_replied'] = topic.has_replied(request.user)
    return render(request, template_name, ext_ctx)
    
def post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return HttpResponseRedirect(post.get_absolute_url_ext())
    
    
@csrf_exempt
def markitup_preview(request, template_name="lbforum/markitup_preview.html"):
    return render(request, template_name, {'message': request.POST['data']})


@login_required
def new_post(request, forum_id=None, topic_id=None, form_class=NewPostForm,
        template_name='qishi/post.html'):
    qpost = topic = forum = first_post = preview = None
    post_type = _('topic')
    topic_post = True
    if forum_id:
        forum = get_object_or_404(Forum, pk=forum_id)
    if topic_id:
        post_type = _('reply')
        topic_post = False
        topic = get_object_or_404(Topic, pk=topic_id)
        forum = topic.forum
        first_post = topic.posts.order_by('created_on').select_related()[0]
    if request.method == "POST":
        form = form_class(request.POST, user=request.user, forum=forum,
                topic=topic, ip=request.META['REMOTE_ADDR'])
        preview = request.POST.get('preview', '')
        if form.is_valid() and request.POST.get('submit', ''):
            post = form.save()
            if topic:
                return HttpResponseRedirect(post.get_absolute_url_ext())
            else:
                return HttpResponseRedirect(reverse("lbforum_forum",
                                                    args=[forum.slug]))
    else:
        initial = {}
        qid = request.GET.get('qid', '')
        if qid:
            qpost = get_object_or_404(Post, id=qid)
            initial['message'] = "[quote=%s]%s[/quote]"
            initial['message'] %= (qpost.posted_by.username, qpost.message)
        form = form_class(initial=initial, forum=forum)
    ext_ctx = {
        'forum': forum,
        'form': form,
        'topic': topic,
        'first_post': first_post,
        'post_type': post_type,
        'preview': preview
    }
#    ext_ctx['unpublished_attachments'] = request.user.attachment_set.filter(activated=False)
    ext_ctx['is_new_post'] = True
    ext_ctx['topic_post'] = topic_post
    ext_ctx['session_key'] = request.session.session_key
    return render(request, template_name, ext_ctx)


@login_required
def edit_post(request, post_id, form_class=EditPostForm,
              template_name="qishi/post.html"):
    preview = None
    post_type = _('reply')
    edit_post = get_object_or_404(Post, id=post_id)
    if not (request.user.is_staff or request.user == edit_post.posted_by):
        return HttpResponse(ugettext('no right'))
    if edit_post.topic_post:
        post_type = _('topic')
    if request.method == "POST":
        form = form_class(instance=edit_post, user=request.user,
                          data=request.POST)
        preview = request.POST.get('preview', '')
        if form.is_valid() and request.POST.get('submit', ''):
            edit_post = form.save()
            return HttpResponseRedirect('../')
    else:
        form = form_class(instance=edit_post)
    ext_ctx = {
        'form': form,
        'post': edit_post,
        'topic': edit_post.topic,
        'forum': edit_post.topic.forum,
        'post_type': post_type,
        'preview': preview
    }
#    ext_ctx['unpublished_attachments'] = request.user.attachment_set.filter(activated=False)
    ext_ctx['topic_post'] = edit_post.topic_post
    ext_ctx['session_key'] = request.session.session_key
    return render(request, template_name, ext_ctx)


@login_required
def user_topics(request, user_id,
                template_name='lbforum/account/user_topics.html'):
    view_user = User.objects.get(pk=user_id)
    topics = view_user.topic_set.order_by('-created_on').select_related()
    context = {
        'topics': topics,
        'view_user': view_user
    }

    return render(request, template_name, context)



@login_required
def user_posts(request, user_id,
               template_name='lbforum/account/user_posts.html'):
    view_user = User.objects.get(pk=user_id)
    posts = view_user.post_set.order_by('-created_on').select_related()
    context = {
        'posts': posts,
        'view_user': view_user
    }
    return render(request, template_name, context)



@login_required
def delete_topic(request, topic_id):
    if not request.user.is_staff:
        #messages.error(_('no right'))
        return HttpResponse(ugettext('no right'))
    topic = get_object_or_404(Topic, id=topic_id)
    forum = topic.forum
    topic.delete()
    forum.update_state_info()
    return HttpResponseRedirect(reverse("lbforum_forum", args=[forum.slug]))


@login_required
def delete_post(request, post_id):
    if not request.user.is_staff:
        return HttpResponse(ugettext('no right'))
    post = get_object_or_404(Post, id=post_id)
    topic = post.topic
    post.delete()
    topic.update_state_info()
    topic.forum.update_state_info()
    #return HttpResponseRedirect(request.path)
    return HttpResponseRedirect(reverse("lbforum_topic", args=[topic.id]))
@login_required
def update_topic_attr_as_not(request, topic_id, attr):
    if not request.user.is_staff:
        return HttpResponse(ugettext('no right'))
    topic = get_object_or_404(Topic, id=topic_id)
    if attr == 'sticky':
        topic.sticky = not topic.sticky
    elif attr == 'close':
        topic.closed = not topic.closed
    elif attr == 'hide':
        topic.hidden = not topic.hidden
    elif attr == 'distillate':
        topic.level = 30 if topic.level >= 60 else 60
    topic.save()
    if topic.hidden:
        return HttpResponseRedirect(reverse("lbforum_forum",
                                            args=[topic.forum.slug]))
    else:
        return HttpResponseRedirect(reverse("lbforum_topic", args=[topic.id]))
