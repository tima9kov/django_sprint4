from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm

handler403 = "pages.views.csrf_failure"
handler404 = "pages.views.page_not_found"
handler500 = "pages.views.server_error"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path("pages/", include("pages.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=UserCreationForm,
            success_url=reverse_lazy("blog:index"),
        ),
        name="registration",
    ),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
