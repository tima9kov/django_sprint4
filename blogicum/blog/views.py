from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.db.models.query import QuerySet
from django.http import Http404
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)

from .forms import CommentForm, PostForm
from .models import Category, Comment, Post, User

PAGINATE_COUNT: int = 10


def get_general_posts_filter() -> QuerySet[Any]:
    return Post.objects.select_related(
        'author',
        'location',
        'category',
    ).filter(
        pub_date__lte=timezone.now(),
        is_published=True,
        category__is_published=True,
    ).annotate(
        comment_count=Count('comments')
    ).order_by('-pub_date')


class EditContentMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs) -> HttpResponse:
        if self.get_object().author != request.user:
            return redirect(
                'blog:post_detail',
                post_id=self.kwargs['post_id']
            )
        return super().dispatch(request, *args, **kwargs)


class ValidationMixin:
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class RedirectionPostMixin:
    def get_success_url(self):
        return reverse(
            'blog:post_detail',
            kwargs={'post_id': self.kwargs['post_id']}
        )


class RedirectionProfileMixin:
    def get_success_url(self):
        return reverse(
            'blog:profile',
            kwargs={'username': self.request.user}
        )


class PostMixin:
    model = Post


class PostFormMixin(PostMixin):
    form_class = PostForm


class PostListMixin(PostMixin):
    paginate_by = PAGINATE_COUNT


class PostCreateMixin:
    template_name = 'blog/create.html'


class PostIdCreateMixin(PostCreateMixin):
    pk_url_kwarg = 'post_id'


class PostListView(PostListMixin, ListView):
    template_name = 'blog/index.html'

    def get_queryset(self) -> QuerySet[Any]:
        return get_general_posts_filter()


class PostDetailView(PostMixin, DetailView):
    template_name = 'blog/detail.html'
    pk_url_kwarg = 'post_id'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().select_related(
            'author',
            'location',
            'category',
        )

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        if post.author != self.request.user and (
            post.is_published is False
            or post.category.is_published is False
            or post.pub_date > timezone.now()
        ):
            raise Http404
        return post

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        context['comments'] = self.object.comments.select_related(
            'author'
        )
        return context


class CategoryListView(PostListMixin, ListView):
    template_name = 'blog/category.html'

    def get_queryset(self) -> QuerySet[Any]:
        return get_general_posts_filter().filter(
            category__slug=self.kwargs['category_slug'],
        )

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(
            Category,
            is_published=True,
            slug=self.kwargs['category_slug'],
        )
        return context


class PostCreateView(
    LoginRequiredMixin,
    PostFormMixin,
    PostCreateMixin,
    ValidationMixin,
    RedirectionProfileMixin,
    CreateView,
):
    pass


class PostUpdateView(
    EditContentMixin,
    PostFormMixin,
    PostIdCreateMixin,
    ValidationMixin,
    RedirectionPostMixin,
    UpdateView,
):
    pass


class PostDeleteView(
    EditContentMixin,
    PostMixin,
    PostIdCreateMixin,
    RedirectionProfileMixin,
    DeleteView,
):
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['form'] = PostForm(instance=self.object)
        return context


class ProfilePostListView(PostListMixin, ListView):
    template_name = 'blog/profile.html'

    def get_queryset(self) -> QuerySet[Any]:
        self.author = get_object_or_404(
            User,
            username=self.kwargs['username']
        )
        return Post.objects.select_related(
            'author',
            'location',
            'category',
        ).filter(
            author=self.author
        ).annotate(
            comment_count=Count('comments')
        ).order_by('-pub_date')

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['profile'] = self.author
        return context


class EditProfileUpdateView(
    LoginRequiredMixin,
    RedirectionProfileMixin,
    UpdateView,
):
    model = User
    template_name = 'blog/user.html'
    fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )

    def get_object(self, queryset=None):
        return self.request.user


class CommentMixin(RedirectionPostMixin):
    model = Comment
    template_name = 'blog/comment.html'
    pk_url_kwarg = 'comment_id'


class CommentFormMixin(CommentMixin):
    form_class = CommentForm


class CommentCreateView(LoginRequiredMixin, CommentFormMixin, CreateView):
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(
            get_general_posts_filter(),
            pk=self.kwargs['post_id']
        )
        return super().form_valid(form)


class CommentUpdateView(EditContentMixin, CommentFormMixin, UpdateView):
    pass


class CommentDeleteView(EditContentMixin, CommentMixin, DeleteView):
    pass
