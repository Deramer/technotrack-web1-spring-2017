from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.urls import reverse_lazy

from sberhack import views


app_name = 'sberhack'
urlpatterns = [ url('^$', views.IndexView.as_view(), name='home'),
]
