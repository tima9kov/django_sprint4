from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("",
         views.PostListView.as_view(),
         name="index"
        ),
    path("category/<slug:category_slug>/",
         views.CategoryListView.as_view(),
         name="category_posts"
        ),
]

#посты
urlpatterns += [
    path(
         'posts/create/',
         views.PostCreateView.as_view(),
         name='create_post',
     ),
     path(
         'posts/<int:post_id>/edit/',
         views.PostUpdateView.as_view(),
         name='edit_post',
     ),
     path(
         'posts/<int:post_id>/delete/',
         views.PostDeleteView.as_view(),
         name='delete_post',
     ),
    path(
        'posts/<int:id>/',
        views.PostDetailView.as_view(),
        name='post_detail',
    ),
]

#профиль
urlpatterns += [
    path(
        'profile/edit/',
        views.EditProfileUpdateView.as_view(),
        name='edit_profile',
    ),
    path(
        'profile/<slug:username>/',
        views.ProfilePostListView.as_view(),
        name='profile',
    ),
]