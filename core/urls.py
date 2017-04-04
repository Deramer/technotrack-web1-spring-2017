from django.conf.urls import url
from django.contrib.auth.views import login, logout
from django.urls import reverse_lazy

from core import views


app_name = 'core'
urlpatterns = [ url('^$', views.HomePageView.as_view(), name='home'),
        url('^about/', views.AboutPage.as_view(), name='about'),
        url('^login/', login, {'template_name': 'core/login.html'}, name='login'),
        url('^logout/', logout, {'template_name': 'core/logout.html'}, name='logout'),
        url('^signup/', views.CreateUser.as_view(success_url=reverse_lazy('core:home')), name='register'),
        url('^ajax_refresh_sidebar/', views.RefreshSidebar.as_view(), name='refresh_sidebar'),
]
