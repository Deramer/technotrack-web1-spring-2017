from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from blog.models import Post
from blog.views import _get_order

def index(request):
    return HttpResponse('12345')


class UserPage(DetailView):
    model = get_user_model()
    pk_url_kwarg = 'user_id'
    template_name = 'user/user_page.html'
    context_object_name = 'local_user'


class UserPostList(ListView):
    template_name = 'user/user_post_list.html'
    context_object_name = 'posts'
    
    def get_queryset(self):
        posts = Post.objects.filter(creator_id=self.kwargs['user_id'])
        if 'search' in self.request.GET:
            posts = posts.filter(title__icontains = self.request.GET['search'])
        posts = posts.order_by(_get_order(self.request.GET))
        threshold = 10
        try:
            threshold = int(self.request.GET['max'])
        except (KeyError, ValueError):
            pass
        posts = posts[:threshold]
        return posts

    def get_context_data(self, **kwargs):
        context = super(UserPostList, self).get_context_data(**kwargs)
        context['local_user'] = get_object_or_404(get_user_model(), id=self.kwargs['user_id'])
        context['order_' + _get_order(self.request.GET).replace('-','desc_')] = True
        context['search'] = self.request.GET.get('search', '')
        return context
