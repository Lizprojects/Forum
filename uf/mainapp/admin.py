from django.contrib import admin

from .models import Category, Event, Post, Profile

# Register your models here.

admin.site.register(Post)
admin.site.register(Event)
admin.site.register(Category)
admin.site.register(Profile)
