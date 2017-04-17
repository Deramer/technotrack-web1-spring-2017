from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Sum
from django.forms import ModelForm, Textarea
from django import forms
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView, DetailView, TemplateView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.html import escape

from html import unescape

from .models import Blog, Post, Comment, Category, GenericLike
from .forms import CommentForm, CommentLikeForm


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
        if 'tag' in self.request.GET:
            blogs = blogs.filter(categories__title__in = self.request.GET.getlist('tag')).distinct()
        if 'search' in self.request.GET:
            blogs = blogs.filter(title__icontains = self.request.GET['search'])
        blogs = blogs.order_by(_get_order(self.request.GET))
        threshold = 10
        try:
            threshold = int(self.request.GET['max'])
            threshold = threshold if threshold > 0 else 10
        except (KeyError, ValueError):
            pass
        self.kwargs['paginator'] = Paginator(blogs, threshold)
        try:
            blogs = self.kwargs['paginator'].page(self.request.GET['page']).object_list
        except (KeyError, ValueError, EmptyPage, PageNotAnInteger):
            blogs = self.kwargs['paginator'].page(1).object_list
        return blogs

    def get_context_data(self, **kwargs):
        context = super(BlogList, self).get_context_data()
        context['order_' + _get_order(self.request.GET).replace('-','desc_')] = True
        context['search'] = self.request.GET.get('search', '')
        try:
            context['page_obj'] = self.kwargs['paginator'].page(int(self.request.GET['page']))     # yeah, I checked, get_queryset is called before get_context_data
        except (KeyError, ValueError, EmptyPage, PageNotAnInteger):
            context['page_obj'] = self.kwargs['paginator'].page(1)
        context['unpaged_link'] = reverse('blog:index')
        context['categories'] = Category.objects.all()
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
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    template_name = 'blog/show_post.html'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs)
        context['blog'] = get_object_or_404(Blog, id=self.kwargs['blog_id'])
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        context['comments'] = Comment.objects.filter(post_id=self.kwargs['post_id'])
        context['post_ct_id'] = ContentType.objects.get_for_model(Post).id
        context['comment_ct_id'] = ContentType.objects.get_for_model(Comment).id
        return context


@method_decorator(login_required, name='dispatch')
class CreateBlog(CreateView):
    model = Blog
    fields = ['title', 'categories',]
    template_name = 'blog/create_blog.html'

    def form_valid(self, form):
        form.instance.creator = self.request.user
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


@method_decorator(login_required, name='dispatch')
class GetCommentForm(CreateView):
    template_name = 'blog/comment_form.html'
    form_class = CommentForm

    def get_initial(self):
        initial = super(GetCommentForm, self).get_initial()
        try:
            initial['parent_id'] = int(self.request.GET['parent_id'])
        except (ValueError, KeyError):
            initial['parent_id'] = -1
        return initial
    
    def get_success_url(self):
        return reverse('blog:show_post', kwargs={'blog_id': self.kwargs['blog_id'], 'post_id': self.kwargs['post_id']})

    def form_valid(self, form):
        form.instance.creator = self.request.user
        if form.cleaned_data['parent_id'] != -1:
            form.instance.parent = Comment.objects.get(id=int(form.cleaned_data['parent_id']))
        else:
            form.instance.parent = None
        form.instance.post = Post.objects.get(id=self.kwargs['post_id'])
        return super(GetCommentForm, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class CreateLike(View):
    def post(self, request, *args, **kwargs):
        if 'model' not in request.POST or 'id' not in request.POST or 'status' not in request.POST:
            return JsonResponse({'result': 'Error: model, id or status not in data'})
        try:
            ct = ContentType.objects.get_for_id(request.POST['model'])
        except ObjectDoesNotExist:
            return JsonResponse({'result': 'Error: model does not exist'})
        try:
            obj = ct.get_object_for_this_type(id=request.POST['id'])
        except ObjectDoesNotExist:
            return JsonResponse({'result': 'Error: no object with such id'})
        try:
            if (int(request.POST['status'])) not in [-1, 1]:
                return JsonResponse({'result': 'Error: status must be either 1 or -1'})
        except ValueError:
            return JsonResponse({'result': 'Error: status must be int'})
        try:
            like = GenericLike.objects.get(content_type=ct, object_id=request.POST['id'], user=request.user)
            like.status = request.POST[ 'status' ]
            like.save()
        except ObjectDoesNotExist:
            like = GenericLike(content_type=ct, object_id=request.POST['id'], user=request.user, status=int(request.POST['status']))
            like.save()
        response = {'result': 'OK'}
        try:
            obj.update_likes_num()
            response['likes_num'] = obj.likes_num
        except AttributeError:
            all_likes = GenericLike.objects.filter(content_type=ct, object_id=request.POST['id'])
            response['likes_num'] = all_likes.aggregate(Sum('status'))['status__avg']
        if ct.model == 'comment':
            response['downvoted'] = True if obj.status == Comment.DOWNVOTED_COMMENT else False
        return JsonResponse(response)
