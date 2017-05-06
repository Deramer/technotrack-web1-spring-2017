from django.conf.urls import url

from quizlet import views


app_name = 'quizlet'
urlpatterns = [ url(r'^$', views.IndexView.as_view(), name = 'index'), 
        url(r'^ajax/$', views.RefreshView.as_view(), name='ajax'),
]
