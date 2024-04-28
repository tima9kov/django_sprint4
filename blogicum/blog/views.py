from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from blog.models import Category, Post
from datetime import datetime as dt
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.http import Http404

CURRENT_TIME = timezone.now()
PUBLICATIONS_ON_MAIN = 5

class PostListView(ListView):
    model = Post
    ordering = 'id'
    paginate_by = PUBLICATIONS_ON_MAIN
    template_name = "blog/index.html"

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'category', 'location'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=CURRENT_TIME
        )


class PostDetailView(DetailView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = "blog/detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related(
            'author', 'category', 'location'
        )

    def get_object(self, queryset = None):
        post =  super().get_object(queryset)

        if post.author != self.request.user and (
            post.is_published is False
            or post.category.is_published is False
            or post.pub_date > CURRENT_TIME
        ):
            raise Http404
        return post

class CategoryListView(ListView):
    model=Post
    ordering = 'id'
    paginate_by = PUBLICATIONS_ON_MAIN
    template_name="blog/category.html"

    def get_queryset(self):
        return Post.objects.select_related(
            'author', 'category', 'location'
        ).filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=CURRENT_TIME,
            category__slug=self.kwargs['category_slug']          
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug']
        )
        return context
