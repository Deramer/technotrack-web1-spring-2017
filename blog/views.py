from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape

from html import unescape

from .models import Blog, Post, Comment


def _get_order(get):
    entity = {'updated': 'updated_at', 'title': 'title'}
    way = {'asc': '', 'desc': '-'}
    order = ''
    order += way.get(get.get('order_way', 'desc'), '-')
    order += entity.get(get.get('order', 'updated'), 'updated_at')
    return order

class BlogList(ListView):
    def get_queryset(self):
        blogs = Blog.objects
        if 'search' in self.request.GET:
            blogs = blogs.filter(title__icontains = self.request.GET['search'])
        blogs = blogs.order_by(_get_order(self.request.GET))
        threshold = 10
        try:
            threshold = int(self.request.GET['max'])
        except (KeyError, ValueError):
            pass
        self.kwargs['pages_num'] = int(blogs.count()/threshold) + 1
        if 'page' in self.kwargs and int(self.kwargs['page']) != 0:
            blogs = blogs[(int(self.kwargs['page'])-1)*threshold : int(self.kwargs['page'])*threshold]
        else:
            blogs = blogs[:threshold]
        return blogs

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data()
        context['order_' + _get_order(self.request.GET).replace('-','desc_')] = True
        context['search'] = self.request.GET.get('search', '')
        context['pages_num'] = self.kwargs['pages_num']     # yeah, I checked, get_queryset is called before get_context_data
        try:
            context['cur_page'] = int(self.kwargs.get('page', None))
        except TypeError as e:
            context['cur_page'] = None
        return context


class PostList(ListView):
    template_name = 'blog/show_blog.html'
    context_object_name = 'posts'

    def get_queryset(self):
        posts = Post.objects.filter(blog_id=self.kwargs['blog_id'])
        if 'search' in self.request.GET:
            posts = posts.filter(title__icontains = self.request.GET['search'])
        if 'user_id' in self.kwargs:
            posts = posts.filter(creator_id=self.kwargs['user_id'])
        posts = posts.order_by(_get_order(self.request.GET))
        threshold = 10
        try:
            threshold = int(self.request.GET['max'])
        except (KeyError, ValueError):
            pass
        posts = posts[:threshold]
        return posts

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, id=self.kwargs['blog_id'])
        context['order_' + _get_order(self.request.GET).replace('-','desc_')] = True
        context['search'] = self.request.GET.get('search', '')
        return context


class PostView(DetailView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, id=self.kwargs['blog_id'])
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['post_id'])
        return context


@method_decorator(login_required, name='dispatch')
class CreateBlog(CreateView):
    model = Blog
    fields = ['title',]
    template_name = 'blog/create_blog.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.title = escape(form.instance.title)
        return super(CreateBlog, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:show_blog', kwargs={'blog_id': self.object.id})


@method_decorator(login_required, name='dispatch')
class CreatePost(CreateView):
    model = Post
    fields = ['title', 'text',]
    template_name = 'blog/create_post.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
        form.instance.blog = get_object_or_404(Blog, id=self.kwargs['blog_id'])
        form.instance.text = escape(form.instance.text).replace('\n', '<br>')
        return super(CreatePost, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:show_post', kwargs={'post_id': self.object.id, 'blog_id': self.kwargs['blog_id']})


@method_decorator(login_required, name='dispatch')
class UpdatePost(UpdateView):
    model = Post
    pk_url_kwarg = 'post_id'
    fields = ['title', 'text',]
    template_name = 'blog/update_post.html'

    def get_success_url(self):
        return reverse('blog:show_post', kwargs={'post_id': self.kwargs['post_id'], 'blog_id': self.kwargs['blog_id']})

    def dispatch(self, request, post_id=None, blog_id=None, *args, **kwargs):
        user = request.user
        self.kwargs['post_id'], self.kwargs['blog_id'] = post_id, blog_id
        post = get_object_or_404(Post, id=post_id)
        if user == post.creator:
            return super(UpdatePost, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('blog:post_update_forbidden', blog_id=self.kwargs['blog_id'], post_id=self.kwargs['post_id'])

    def get_initial(self):
        init = super(UpdatePost, self).get_initial()
        init['text'] = unescape(get_object_or_404(Post, id=self.kwargs['post_id']).text.replace('<br>', '\n'))
        return init
    
    def form_valid(self, form):
        form.instance.text = escape(form.instance.text).replace('\n', '<br>')
        return super(UpdatePost, self).form_valid(form)


class PostUpdateForbidden(TemplateView):
    template_name = 'blog/post_update_forbidden.html'

    def get_context_data(self, **kwargs):
        context = super(PostUpdateForbidden, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        context['blog'] = get_object_or_404(Blog, id=self.kwargs['blog_id'])
        return context

@method_decorator(login_required, name='dispatch')
class DeletePost(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    template_name = 'blog/delete_post.html'

    def get_success_url(self):
        return reverse('blog:show_blog', kwargs={'blog_id': self.kwargs['blog_id']})

    def dispatch(self, request, blog_id=None, post_id=None, *args, **kwargs):
        self.kwargs['post_id'] = post_id
        self.kwargs['blog_id'] = blog_id
        if request.user == get_object_or_404(Post, id=post_id).creator:
            return super(DeletePost, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('blog:post_deletion_forbidden', blog_id=blog_id, post_id=post_id)


class PostDeletionForbidden(TemplateView):
    template_name = 'blog/post_deletion_forbidden.html'

    def get_context_data(self, **kwargs):
        context = super(PostDeletionForbidden, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, id=self.kwargs['post_id'])
        context['blog'] = get_object_or_404(Blog, id=self.kwargs['blog_id'])
        return context


@method_decorator(login_required, name='dispatch')
class DeleteBlog(DeleteView):
    model = Blog
    pk_url_kwarg = 'blog_id'
    template_name = 'blog/delete_blog.html'

    def get_success_url(self):
        return reverse('blog:index')

    def dispatch(self, request, blog_id=None, *args, **kwargs):
        self.kwargs['blog_id'] = blog_id
        if request.user == get_object_or_404(Blog, id=blog_id).creator:
            return super(DeleteBlog, self).dispatch(request, *args, **kwargs)
        else:
            return redirect('blog:blog_deletion_forbidden', blog_id=blog_id)


class BlogDeletionForbidden(TemplateView):
    template_name = 'blog/blog_deletion_forbidden.html'

    def get_context_data(self, **kwargs):
        context = super(BlogDeletionForbidden, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, id=self.kwargs['blog_id'])
        return context
