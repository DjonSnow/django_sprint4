from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('category/<slug:slug>/', views.category_posts, name='category_posts'),
    path(
        'auth/registration/',
        views.register,
        name='registration'
    ),
    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile',
    ),
    path(
        'profile/<str:username>/',
        views.profile,
        name='profile'
    ),
    path(
    'posts/create/',
    views.create_post,
    name='create_post'
    ),
    path(
    'posts/<int:post_id>/edit/',
    views.edit_post,
    name='edit_post'
    ),
    path(
    'posts/<int:post_id>/comment/',
    views.add_comment,
    name='add_comment'
    ),
    path(
    'posts/<int:post_id>/edit_comment/<int:comment_id>/',
    views.edit_comment,
    name='edit_comment'
    ),
    path(
    'posts/<int:post_id>/delete/',
    views.delete_post,
    name='delete_post'
    ),
    path(
    'posts/<int:post_id>/delete_comment/<int:comment_id>/',
    views.delete_comment,
    name='delete_comment'
    ),
    path(
    'about/',
    TemplateView.as_view(template_name='pages/about.html'),
    name='about'
    ),
    path(
    'rules/',
    TemplateView.as_view(template_name='pages/rules.html'),
    name='rules'
    ),
]

handler404 = 'blog.views.page_not_found'
handler500 = 'blog.views.server_error'
