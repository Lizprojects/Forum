from dataclasses import field, fields
from multiprocessing import context

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
)
from django.views.generic.base import RedirectView
from django.views.generic.edit import FormMixin

from .forms import (
    EventCreationForm,
    PostCreationForm,
    StudentProfileUpdateForm,
    UserCreationForm,
)
from .models import Category, Event, Post, Profile

# Create your views here.

# HOME REDIRECT nelage jodi remove koridibi


class HomeRedirect(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if user.is_authenticated:
            return reverse("mainapp:home")
        return reverse("mainapp:signup")


# HOME METHOD nelage jodi remove koridibi


def home(request):
    context = {"posts": Post.objects.all()}
    return render(request, "mainapp/home.html", context)


# SIGNUP-LOGIN-HOMEPAGE


class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = "mainapp/signup.html"
    success_url = reverse_lazy("mainapp:signin")


class StudentLoginView(LoginView):
    template_name = "mainapp/signin.html"

    def get_success_url(self):
        return reverse("mainapp:home")


class PostListView(ListView):
    model = Post
    template_name = "mainapp/home.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "posts"
    ordering = ["-dandt"]
    paginate_by = 2

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(PostListView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context


class StudentLogoutView(LogoutView):
    template_name = "mainapp/signin.html"


# SEARCH POST BY TITLE/CONTENT


def searchpost(request):
    query = request.GET["query"]
    if len(query) > 78:
        posts = Post.objects.none()
    else:
        poststitle = Post.objects.filter(title__icontains=query)
        postscontent = Post.objects.filter(content__icontains=query)
        posts = poststitle.union(postscontent)

    if posts.count() == 0:
        messages.warning(request, "Please enter valid query")
    params = {"posts": posts, "query": query}
    return render(request, "mainapp/searchpost.html", params)


# SEARCH EVENT BY TITLE/CONTENT


def searchevent(request):
    query = request.GET["query"]
    if len(query) > 78:
        events = Event.objects.none()
    else:
        eventstitle = Event.objects.filter(title__icontains=query)
        eventscontent = Event.objects.filter(content__icontains=query)
        events = eventstitle.union(eventscontent)

    if events.count() == 0:
        messages.warning(request, "Please enter valid query")
    params = {"events": events, "query": query}
    return render(request, "mainapp/searchevent.html", params)


# STUDENT PROFILE-UPDATE/PASSWORD CHANGE


class ShowProfileView(DetailView):
    model = Profile
    template_name = "mainapp/showprofile.html"

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(StudentProfileView, self).get_context_data(*args, **kwargs)

        page_user = get_object_or_404(Profile, id=self.kwargs["pk"])

        context["page_user"] = page_user
        return context


class StudentProfileView(CreateView):
    model = Profile
    template_name = "mainapp/profile.html"
    # success_message = "Your profile has been updated successfully."
    success_url = reverse_lazy("mainapp:profile")
    fields = (
        "profile_pic",
        "bio",
        "websiteurl",
        "fburl",
        "twitterurl",
        "igurl",
    )

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        instance = form.instance
        instance.user = self.request.user
        return super().form_valid(form)


class StudentProfileUpdateView(UpdateView):
    model = Profile
    form_class = StudentProfileUpdateForm
    template_name = "mainapp/profile_update.html"

    def get_success_url(self):
        return reverse("mainapp:profile-update", kwargs={"pk": self.object.pk})



    def get_initial(self):
        user=self.request.user
        initial = super().get_initial()
        initial.update({
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        })
        return initial

    def form_valid(self, form):
        self.object.update_user(form.cleaned_data, form.changed_data)
        message = 'Your profile has been updated'
        messages.success(self.request, message)
        return super().form_valid(form)

    


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy("mainapp:password_success")


def password_success(request):
    return render(request, "mainapp/password_success.html", {})


# POST-CREATION/DETAILS/UPDATION/DELETION


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreationForm
    template_name = "mainapp/post_form.html"
    success_url = reverse_lazy("mainapp:home")

    def form_valid(self, form):
        instance = form.instance
        instance.author = self.request.user
        return super().form_valid(form)


class PostDetailView(DetailView):
    model = Post
    template_name = "mainapp/post_detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(PostDetailView, self).get_context_data(*args, **kwargs)
        stuff = get_object_or_404(Post, id=self.kwargs["pk"])
        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True
        total_likes = stuff.total_likes()
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context


class PostUpdateView(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "mainapp/post_update.html"
    success_url = reverse_lazy("mainapp:home")
    fields = ("title", "filecon", "content")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(UserPassesTestMixin, DeleteView, FormMixin):
    model = Post
    template_name = "mainapp/post_delete.html"
    success_url = reverse_lazy("mainapp:home")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# POST LIKE/UNLIKE


def PostLikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get("post_id"))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse("mainapp:post-detail", args=[str(pk)]))


# CATEGORY CREATION/ CATEGORY LIST


class CategoryCreateView(CreateView):
    model = Category
    template_name = "mainapp/add_category.html"
    fields = "__all__"
    success_url = reverse_lazy("mainapp:home")


def CategoryView(request, category):
    category_posts = Post.objects.filter(category=category)
    return render(
        request,
        "mainapp/categories.html",
        {"category": category.title(), "category_posts": category_posts},
    )


# def CategoryListView(request):
#     cat_menu_list = Category.objects.all()


# EVENTS CREATION/DETAILS/UPDATION/DELETION


class EventListView(ListView):
    model = Event
    template_name = "mainapp/events.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "events"
    ordering = ["-dandt"]
    paginate_by = 2


class EventCreateView(CreateView):
    model = Event
    form_class = EventCreationForm
    template_name = "mainapp/event_form.html"
    success_url = reverse_lazy("mainapp:event-list")

    def form_valid(self, form):
        instance = form.instance
        instance.author = self.request.user
        return super().form_valid(form)


class EventDetailView(DetailView):
    model = Event
    template_name = "mainapp/event_detail.html"

    # def get_object(self, queryset=None):
    #     return get_object_or_404(Event, pk=self.kwargs.get("pk"))
    # def get_context_data(self, **kwargs):
    #     return super().get_context_data(**kwargs)


class EventUpdateView(UserPassesTestMixin, UpdateView):
    model = Event
    template_name = "mainapp/event_update.html"
    success_url = reverse_lazy("mainapp:event-list")
    fields = ("title", "content")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user == event.author:
            return True
        return False


class EventDeleteView(UserPassesTestMixin, DeleteView, FormMixin):
    model = Event
    template_name = "mainapp/event_delete.html"
    success_url = reverse_lazy("mainapp:event-list")

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
