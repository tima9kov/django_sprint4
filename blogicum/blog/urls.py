from django.urls import path

from . import views

app_name: str = "blog"

urlpatterns: list = [
    path("", views.PostListView.as_view(), name="index"),
    path(
        "category/<slug:category_slug>/",
        views.CategoryListView.as_view(),
        name="category_posts",
    ),
]

# urls for posts
urlpatterns += [
    path(
        "posts/create/",
        views.PostCreateView.as_view(),
        name="create_post",
    ),
    path(
        "posts/<int:post_id>/edit/",
        views.PostUpdateView.as_view(),
        name="edit_post",
    ),
    path(
        "posts/<int:post_id>/delete/",
        views.PostDeleteView.as_view(),
        name="delete_post",
    ),
    path(
        "posts/<int:post_id>/",
        views.PostDetailView.as_view(),
        name="post_detail",
    ),
]

# urls for comments
urlpatterns += [
    path(
        "posts/<int:post_id>/comment/",
        views.CommentCreateView.as_view(),
        name="add_comment",
    ),
    path(
        "posts/<int:post_id>/edit_comment/<int:comment_id>/",
        views.CommentUpdateView.as_view(),
        name="edit_comment",
    ),
    path(
        "posts/<int:post_id>/delete_comment/<int:comment_id>/",
        views.CommentDeleteView.as_view(),
        name="delete_comment",
    ),
]

# urls for profile
urlpatterns += [
    path(
        "profile/edit/",
        views.EditProfileUpdateView.as_view(),
        name="edit_profile",
    ),
    path(
        "profile/<slug:username>/",
        views.ProfilePostListView.as_view(),
        name="profile",
    ),
]
