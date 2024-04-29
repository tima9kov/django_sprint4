from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("",
         views.PostListView.as_view(),
         name="index"
        ),
    path("posts/<int:id>/",
         views.PostDetailView.as_view(),
         name="post_detail"
        ),
    path("category/<slug:category_slug>/",
         views.CategoryListView.as_view(),
         name="category_posts"
        ),
    path("profile/<slug:username>",
         views.ProfilePostListView.as_view(),
         name='profile'
    )
]
