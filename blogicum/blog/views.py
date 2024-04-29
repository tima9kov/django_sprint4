from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Category, Post, User
from datetime import datetime as dt
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.http import Http404
from .forms import PostForm

CURRENT_TIME = timezone.now()
PUBLICATIONS_ON_MAIN = 5


def get_published_posts():
    return Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=CURRENT_TIME
    ).order_by(
        '-pub_date'
    )


class PostMixin():
    model = Post


class PostFormMixin(PostMixin):
    form_class = PostForm


class PostListMixin(PostMixin):
    paginate_by = PUBLICATIONS_ON_MAIN


#CBV для навбара
class PostListView(PostListMixin, ListView):
    template_name = "blog/index.html"

    def get_queryset(self):
        return get_published_posts()


class PostDetailView(PostMixin, DetailView):
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

class CategoryListView(PostListMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self):
        return get_published_posts().filter(
            category__slug=self.kwargs['category_slug'],
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug'],
        )
        return context

#CBV для профиля
class ProfilePostListView(PostListMixin, ListView):
    template_name='blog/profile.html'
    
    def get_queryset(self):
        self.author=get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return Post.objects.select_related(
            'author', 'location', 'category',
        ).filter(
            author=self.author
        ).order_by('-pub_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context

class EditProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name='blog/user.html'
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


#CBV для постов
class PostCreateView(CreateView):
    pass

class PostUpdateView(UpdateView):
    pass

class PostDeleteView(DeleteView):
    pass

#CBV для комментариев