from django.conf.urls import url

from user import views


app_name = 'user'
urlpatterns = [ url(r'^$', views.index, name = 'index'), 
        url(r'^(?P<user_id>\d+)/$', views.UserPage.as_view(), name='user_page'),
        url(r'^(?P<user_id>\d+)/subscribe/$', views.SubscribeView.as_view(), name='subscribe'),
        url(r'^(?P<user_id>\d+)/posts/$', views.UserPostList.as_view(), name='user_posts'),
]
