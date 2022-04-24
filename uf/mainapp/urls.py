from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "mainapp"

urlpatterns = [
    path("home/", views.PostListView.as_view(), name="home"),
    path(
        "",
        views.HomeRedirect.as_view(),
        name="homeredirect",
    ),
    # path(
    #     "<int:pk>/view-profile/",
    #     views.ShowProfileView.as_view(),
    #     name="view-profile",
    # ),
    # path("profile/<int:pk/", views.StudentProfileView.as_view(), name="profile"),
    path(
        "<int:pk>/profile_update/",
        views.StudentProfileUpdateView.as_view(),
        name="profile-update",
    ),
    path(
        "password/",
        views.PasswordsChangeView.as_view(template_name="mainapp/change_pass.html"),
    ),
    path("password_success/", views.password_success, name="password_success"),
    path("signup", views.SignupView.as_view(), name="signup"),
    path("signin", views.StudentLoginView.as_view(), name="signin"),
    path("signout", views.StudentLogoutView.as_view(), name="signout"),
    path("search/", views.searchpost, name="searchpost"),
    path("searchevent/", views.searchevent, name="searchevent"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("post_form/", views.PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update/", views.PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", views.PostDeleteView.as_view(), name="post-delete"),
    path("add_category/", views.CategoryCreateView.as_view(), name="add-category"),
    path("category/<str:category>/", views.CategoryView, name="category"),
    path("event/", views.EventListView.as_view(), name="event-list"),
    path("event_create/", views.EventCreateView.as_view(), name="event-create"),
    path("event/<int:pk>/", views.EventDetailView.as_view(), name="event-detail"),
    path(
        "event/<int:pk>/update/", views.EventUpdateView.as_view(), name="event-update"
    ),
    path(
        "event/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event-delete"
    ),
    path("like/<int:pk>", views.PostLikeView, name="like-post"),
]


