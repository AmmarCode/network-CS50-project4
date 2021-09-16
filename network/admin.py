from django.contrib import admin

from .models import User, Following, Post
# Register your models here.
admin.site.register(User)
admin.site.register(Following)
admin.site.register(Post)