from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.forms import ModelForm, ValidationError
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.shortcuts import render

from datetime import datetime

from user.models import User
from blog.models import Blog, Post, Comment


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'avatar']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        email = cleaned_data.get('email')
        if password:
            validate_password(password)
        if email is not None: 
            if len(email) == 0:
                raise ValidationError('Enter email.')


class CreateUser(CreateView):
    form_class = UserForm
    template_name = 'core/user_form.html'

    def form_valid(self, form):
        form.instance.password = make_password(form.instance.password)
        return super(CreateUser, self).form_valid(form)


class HomePageView(TemplateView):
    template_name = 'core/homepage.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['blog_num'] = Blog.objects.count()
        context['post_num'] = Post.objects.count()
        context['comment_num'] = Comment.objects.count()
        return context


class AboutPage(TemplateView):
    template_name = 'core/aboutpage.html'


class RefreshSidebar(TemplateView):
    template_name = 'core/sidebar.html'

    def get_context_data(self, **kwargs):
        try:
            dt = datetime.utcfromtimestamp(float(self.request.GET['from_time']))
        except (KeyError, ValueError):
            raise ValidationError('What?')
            return super(RefreshSidebar, self).get_context_data(**kwargs)
        context = super(RefreshSidebar, self).get_context_data(**kwargs)
        context['list'] = Post.objects.filter(created_at__gte=dt).order_by('-created_at')[:9]
        context['timestamp'] = datetime.utcnow().timestamp()
        return context
