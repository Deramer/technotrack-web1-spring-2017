from django.conf.urls import url

from blog import views


app_name = 'blog'
urlpatterns = [ url(r'^$', views.BlogList.as_view(), name = 'index'),
        url(r'^page(?P<page>\d+)/$', views.BlogList.as_view(), name = 'index_page'),
        url(r'^create/', views.CreateBlog.as_view(), name='create_blog'),
        url(r'^(?P<blog_id>\d+)/$', views.PostList.as_view(), name = 'show_blog'),
        url(r'^(?P<blog_id>\d+)/create', views.CreatePost.as_view(), name='create_post'),
        url(r'^(?P<blog_id>\d+)/delete', views.DeleteBlog.as_view(), name='delete_blog'),
        url(r'^(?P<blog_id>\d+)/deletion_forbidden', views.BlogDeletionForbidden.as_view(), name='blog_deletion_forbidden'),
        url(r'^(?P<blog_id>\d+)/(?P<post_id>\d+)/$', views.PostView.as_view(), name='show_post'),
        url(r'^(?P<blog_id>\d+)/(?P<post_id>\d+)/update/', views.UpdatePost.as_view(), name='update_post'),
        url(r'^(?P<blog_id>\d+)/(?P<post_id>\d+)/update_forbidden/', 
            views.PostUpdateForbidden.as_view(), name='post_update_forbidden'),
        url(r'^(?P<blog_id>\d+)/(?P<post_id>\d+)/delete/', views.DeletePost.as_view(), name='delete_post'),
        url(r'^(?P<blog_id>\d+)/(?P<post_id>\d+)/deletion_forbidden/', 
            views.PostDeletionForbidden.as_view(), name='post_deletion_forbidden'),
        url(r'^(?P<blog_id>\d+)/(?P<post_id>\d+)/ajax_comment_form', views.GetCommentForm.as_view(), name='comment_form'),
]
