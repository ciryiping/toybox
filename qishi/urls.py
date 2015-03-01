from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url, include

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from qishi import views


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
#    url('^(?P<topic_id>\d+)/delete/$', views.delete_topic,
#        name='lbforum_delete_topic'),
#    url('^(?P<topic_id>\d+)/update_topic_attr_as_not/(?P<attr>[\w-]+)/$',
#        views.update_topic_attr_as_not,
#        name='lbforum_update_topic_attr_as_not'),
#    url('^new/(?P<forum_id>\d+)/$', views.new_post, name='lbforum_new_topic'),
)

urlpatterns = patterns('',
    url(r'^forum/', include(forum_patterns)),
    url(r'^topic/', include(topic_patterns)),
    url(r'^admin/?$',    views.admin,          name="admin"   ),
    url(r'^register/?$', views.register,       name="register"),
    url(r'^login/?$',    views.my_login,          name="login"   ),
    url(r'^logoff/?$',   views.logoff,         name="logoff"  ),        
    url(r'^$',           views.index,          name="index"   ),
    url(r'',             views.page_not_found, name="http404" ),
    )# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
