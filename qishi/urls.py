from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, url

from qishi import views

urlpatterns = patterns('',
    url(r'^admin/?$',    views.admin,          name="admin"   ),
    url(r'^register/?$', views.register,       name="register"),
    url(r'^login/?$',    views.login,          name="login"   ),
    url(r'^logoff/?$',   views.logoff,         name="logoff"  ),        
    url(r'^$',           views.index,          name="index"   ),
    url(r'',             views.page_not_found, name="http404" ),
    )# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
