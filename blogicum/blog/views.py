from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now
from .models import Post, Category, Location, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .forms import PostForm, CommentForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.urls import reverse

from .querysets import get_page_obj, published_posts, with_comment_count


User = get_user_model()


def index(request):
    posts = Post.objects.select_related(
        'author',
        'category',
        'location',
    )
    post_list = with_comment_count(published_posts(posts))
    page_obj = get_page_obj(request, post_list)

    return render(
        request,
        'blog/index.html',
        {'page_obj': page_obj}
    )


def category_posts(request, slug):
    category = get_object_or_404(
        Category,
        slug=slug,
        is_published=True,
    )
    posts = category.post_set.select_related('author', 'category', 'location')
    post_list = with_comment_count(published_posts(posts))
    page_obj = get_page_obj(request, post_list)

    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'page_obj': page_obj,
        }
    )


def post_detail(request, post_id):
    base_qs = Post.objects.select_related(
        'author',
        'category',
        'location',
    )
    post = get_object_or_404(base_qs, id=post_id, category__isnull=False)

    if post.author != request.user:
        # Second get_object_or_404 ensures access control is defined by the
        # published posts queryset.
        post = get_object_or_404(
            published_posts(base_qs),
            id=post_id,
        )

    comments = post.comments.select_related('author').order_by('created')
    form = CommentForm()

    return render(request, 'blog/detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })


def csrf_failure(request, reason=''):
    return render(request, 'pages/403csrf.html', status=403)


def page_not_found(request, exception):
    return render(request, 'pages/404.html', status=404)


def server_error(request):
    return render(request, 'pages/500.html', status=500)


def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'registration/registration_form.html', {'form': form})


def profile(request, username):
    user = get_object_or_404(User, username=username)

    posts = user.post_set.select_related(
        'author',
        'category',
        'location',
    ).filter(
        category__isnull=False,
    )

    if request.user != user:
        posts = published_posts(posts)

    posts = with_comment_count(posts)
    page_obj = get_page_obj(request, posts)

    return render(
        request,
        'blog/profile.html',
        {
            'profile_user': user,
            'page_obj': page_obj,
        }
    )


@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if form.is_valid():
        form.save()
        return redirect('blog:profile', username=request.user.username)
    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('blog:profile', username=request.user.username)
    return render(
        request,
        'blog/create.html',
        {'form': form}
    )


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', post_id=post.id)

    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
        instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post.id)

    return render(
        request,
        'blog/create.html',
        {'form': form, 'post': post}
    )


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect(
        'blog:post_detail',
        post_id=post.id
    )


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        post_id=post_id,
        author=request.user
    )

    form = CommentForm(request.POST or None, instance=comment)
    if form.is_valid():
        form.save()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'form': form, 'comment': comment})



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        author=request.user
    )

    if request.method == 'POST':
        post.delete()
        return redirect('blog:index')

    form = PostForm(instance=post)
    return render(
        request,
        'blog/create.html',
        {'form': form, 'post': post, 'is_delete': True},
    )




@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(
        Comment,
        id=comment_id,
        post_id=post_id,
        author=request.user
    )

    if request.method == 'POST':
        comment.delete()
        return redirect('blog:post_detail', post_id=post_id)

    return render(request, 'blog/comment.html', {'comment': comment, 'is_delete': True})

