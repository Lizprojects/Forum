from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse_lazy
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, primary_key = True, null=False, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(
        default="static/default/default.png", upload_to="profile_pics/"
    )
    websiteurl = models.CharField(max_length=200, blank=True, null=True)
    fburl = models.CharField(max_length=200, blank=True, null=True)
    twitterurl = models.CharField(max_length=200, blank=True, null=True)
    igurl = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def update_user(self, cleaned_data, changed_data):
        user=self.user
        data = {field: cleaned_data[field]
                for field in ('first_name', 'last_name', 'email', 'username')
                if field in changed_data}
        if data:
            for field, value in data.items():
                setattr(user, field, value)
            user.save()


class Category(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse_lazy("home")


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField(blank=True, null=True)
    category = models.CharField(max_length=200, default="uncategorised")
    dandt = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    filecon = models.FileField(blank=True, null=True, upload_to="user_post_files")
    likes = models.ManyToManyField(User, related_name="liked_post")

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("post-detail", args=(str(self.id)))


class Event(models.Model):
    title = models.CharField(max_length=100)
    content = RichTextField(blank=True, null=True)
    dandt = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse_lazy("event-detail", kwargs={"pk": self.pk})
