from django.contrib import admin
from .models import User, Post, Like, Follower

class FollowerAdmin(admin.ModelAdmin):
    list_display = ('followee', 'follower')

admin.site.register(Post)
admin.site.register(Like)
admin.site.register(User)
admin.site.register(Follower, FollowerAdmin)