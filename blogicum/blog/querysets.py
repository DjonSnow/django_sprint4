from __future__ import annotations

from django.core.paginator import Paginator
from django.db.models import Count, QuerySet
from django.http import HttpRequest
from django.utils.timezone import now

from .models import Post


def with_comment_count(posts: QuerySet[Post]) -> QuerySet[Post]:
    return posts.annotate(comment_count=Count("comments")).order_by(
        *Post._meta.ordering
    )


def published_posts(posts: QuerySet[Post] | None = None) -> QuerySet[Post]:
    if posts is None:
        posts = Post.objects.all()
    return posts.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=now(),
        category__isnull=False,
    )


def get_page_obj(
    request: HttpRequest,
    queryset: QuerySet,
    per_page: int = 10,
    page_param: str = "page",
):
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get(page_param)
    return paginator.get_page(page_number)

