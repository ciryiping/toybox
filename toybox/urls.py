from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'toybox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
 
    url(r'^toybox-admin/', include(admin.site.urls)),

    # ===== Qishi Website =====
    url(r'^qishi/', include("qishi.urls")),
)
