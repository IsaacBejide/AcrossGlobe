from django.conf import settings
from django.urls import path, re_path as url
from . import views
from .views import UpdatePostView
from django.conf.urls.static import static
from django.utils.translation import gettext_lazy as _

from django.views.generic import TemplateView
#from posts.views import PostListView, PostDetailView

app_name = 'MyBlog'

urlpatterns = [
    #     blogs
    path("", views.blogs_list, name="blogs"),
    # path("blog/<str:slug>/", views.blogsByCategory, name="blogCategory"),
    # path("blog/<int:cat_id>/", views.blogByCategory, name="blogCategory"),
    path(_('add_category/'), views.add_category, name="category"),
    # path("blog/<str:slug>/", views.blogs_comments, name="blogs_comments"),
    path(_('blog/<str:slug>/'), views.blog_details, name="blog_details"),
    #path('<slug:slug>/', PostDetailView.as_view(), name='detail'),
    path(_('blog/<str:slug>/<int:cat_id>/'), views.blogByCategory, name="blogs_Category"),

    path(_('like/'), views.post_like, name='like'),

    path(_('newtopic/<int:cat_id>/'), views.add_newtopic, name="add_newtopic"),
    path(_('add_comment/<str:slug>/'), views.add_comment, name="add_comment"),
    path(_('reply_comment/<int:comment_id>/'), views.reply_comment, name="reply_comment"),
    path(_('advertisement/<int:category_id>/'), views.advertisement, name="advertisement"),
    #path(_('reply_comment/<str:slug>/<int:comment_id>/'), views.reply_comment, name="reply_comment"),

    path(_('edit_blog_post/<str:slug>/'), views.update_post, name="update_post"),
    path(_('edit_blog_post/<str:slug>/'), UpdatePostView.as_view(), name="edit_blog_post"),
    path(_('delete_blog_post/<str:slug>/'), views.Delete_Blog_Post, name="delete_blog_post"),
    path(_('search/'), views.search, name="search"),


   

    #    user authentication
    #path(_('register/'), views.Register, name="register"),
    #path(_('login/'), views.Login, name="login"),
    path(_('logout/'), views.Logout, name="logout"),

    #   Share post via email
    path('<int:post_id>/share/', views.post_share, name='post_share'),

    #   User's list view. Follow System part
    path(_('users/'), views.user_list, name='user_list'),
    path(_('users/<username>/'), views.user_detail, name='user_detail'),
    
    #   Site Statistics
    path('stat/', views.site_statistics, name='site_statistics'),

    path(_('infinite_scrolling'), views.AllKeywordsView.as_view(template_name="blog.html"), ),



    ###########  Administrative Areas ##################################
    # path(_('admins/'), views.blogsAdmin, name="blogsAdmin"),
    # path(_('admins/<int:cat_id>/'), views.blogsAdminByCategory, name="blogsAdmin"),
    #path(_('admins/blog/<str:slug>/'), views.blogs_comment, name="blogs_comments"),
    #path(_('admins/<int:cat_id>/blog/<str:slug>/'), views.blogs_commentsbyCategory, name="blogs_comments"),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
