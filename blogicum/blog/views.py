from django.shortcuts import render, get_object_or_404
from blog.models import Category, Post
from datetime import datetime as dt

CURRENT_TIME = dt.now()
PUBLICATIONS_ON_MAIN = 5


def index(request):
    post_list = Post.objects.select_related(
        'author', 'location', 'category',
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=CURRENT_TIME).order_by()[:PUBLICATIONS_ON_MAIN]
    return render(request, "blog/index.html", {"post_list": post_list})


def post_detail(request, id):
    post = get_object_or_404(
        Post.objects.select_related(
            'author', 'location', 'category',
        ).filter(
            is_published=True,
            pub_date__lte=CURRENT_TIME,
            category__is_published=True,
            id=id
        )
    )
    return render(request, "blog/detail.html", {"post": post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category.objects.filter(is_published=True, slug=category_slug)
    )
    post_list = Post.objects.select_related(
        'author', 'location', 'category',
    ).filter(
        pub_date__lte=CURRENT_TIME,
        is_published=True,
        category=category,)
    return render(request,
                  "blog/category.html",
                  {'category': category, 'post_list': post_list})
