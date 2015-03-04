from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url, include

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from qishi import views,accountviews


forum_patterns = patterns(
    '',
    url(r'^(?P<forum_slug>[\w-]+)/$', views.forum, name='lbforum_forum'),
    url(r'^(?P<forum_slug>[\w-]+)/(?P<topic_type>[\w-]+)/$',
        views.forum, name='lbforum_forum'),
    url(r'^(?P<forum_slug>[\w-]+)/(?P<topic_type>[\w-]+)/(?P<topic_type2>[\w-]+)/$',
        views.forum, name='lbforum_forum'),
)

topic_patterns = patterns(
    '',
    url('^(?P<topic_id>\d+)/$', views.topic, name='lbforum_topic'),
    url('^(?P<topic_id>\d+)/delete/$', views.delete_topic,
        name='lbforum_delete_topic'),
    url('^(?P<topic_id>\d+)/update_topic_attr_as_not/(?P<attr>[\w-]+)/$',
        views.update_topic_attr_as_not,
        name='lbforum_update_topic_attr_as_not'),
    url('^new/(?P<forum_id>\d+)/$', views.new_post, name='lbforum_new_topic'),
)

post_patterns = patterns(
    '',
    url('^(?P<post_id>\d+)/$', views.post, name='lbforum_post'),
    url('^(?P<post_id>\d+)/edit/$', views.edit_post, name='lbforum_post_edit'),
    url('^(?P<post_id>\d+)/delete/$', views.delete_post,
        name='lbforum_post_delete'),
    url('^reply/new/(?P<topic_id>\d+)/$', views.new_post,
        name='lbforum_new_replay'),
)

urlpatterns = patterns('',
    url(r'^forum/', include(forum_patterns)),
    url(r'^topic/', include(topic_patterns)),
    url(r'^post/', include(post_patterns)),
    url(r'^blogview/',   views.blogview,       name="blogview"),
    url(r'^admin/?$',    views.admin,          name="admin"   ),
    url(r'^register/?$', views.register,       name="register"),
    url(r'^login/?$',    views.my_login,          name="login"   ),
    url(r'^logoff/?$',   views.logoff,         name="logoff"  ),        
    url(r'^$',           views.index,          name="index"   ),
    url(r'',             views.page_not_found, name="http404" ),
    )# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += patterns('',
    url('^user/(?P<user_id>\d+)/topics/$', views.user_topics,
        name='lbforum_user_topics'),
    url('^user/(?P<user_id>\d+)/posts/$', views.user_posts,
        name='lbforum_user_posts'),
    url(r'^user/(?P<user_id>\d+)/$', login_required(accountviews.profile),
        name='lbforum_user_profile'),
)