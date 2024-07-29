from django.contrib import admin
from .models import User, Post, Like, Follower


class FollowerAdmin(admin.ModelAdmin):
    list_display = ('followee', 'follower')


class LikeAdmin(admin.ModelAdmin):
    list_display = ('post_id','post', 'user')

admin.site.register(Post)
admin.site.register(User)
admin.site.register(Like, LikeAdmin)
admin.site.register(Follower, FollowerAdmin)