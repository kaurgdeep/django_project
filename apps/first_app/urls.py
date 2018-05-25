from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^processreg$', views.processreg),
    url(r'^processlog$', views.processlog),
    url(r'^quotes$', views.quotes),
    url(r'^logout$', views.logout),
    url(r'^submit$', views.submit),
    url(r'^posted_others/(?P<user_id>\d+)$', views.posted_others),
    url(r'^posted_me/(?P<user_id>\d+)$', views.posted_others),
    url(r'^add/(?P<quote_id>\d+)$', views.add),
    url(r'^remove/(?P<quote_id>\d+)$', views.remove),
    url(r'^home$', views.home)

      
]                            