from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.forms import UserCreationForm as BaseUserCreationForm
from PIL import Image

from mainapp.models import Category, Event, Post, Profile

choices = Category.objects.all().values_list("name", "name")
choice_list = []

for item in choices:
    choice_list.append(item)


class UserCreationForm(BaseUserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = get_user_model()
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["class"] = "form-control"


class StudentProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )
    username = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Profile
        fields = (
            "profile_pic",
            "bio",
            "websiteurl",
            "fburl",
            "twitterurl",
            "igurl",
        )

        widgets = {
            "profile_pic": forms.FileInput(
                attrs={"class": "form-control"}
            ),
            "bio": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "websiteurl": forms.URLInput(
                attrs={"class": "form-control"}
            ),
            "fburl": forms.URLInput(
                attrs={"class": "form-control"}
            ),
            "twitterurl": forms.URLInput(
                attrs={"class": "form-control"}
            ),
            "igurl": forms.URLInput(
                attrs={"class": "form-control"}
            ),
        }


class PostCreationForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "category", "filecon", "content")

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title of the Post"}
            ),
            "category": forms.Select(
                choices=choice_list, attrs={"class": "form-control"}
            ),
            "filecon": forms.FileInput(
                attrs={"class": "form-control", "placeholder": "Add a File"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Write Something.."}
            ),
        }


class EventCreationForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ("title", "content")

        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Title of the Event"}
            ),
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "What's happening?"}
            ),
        }
