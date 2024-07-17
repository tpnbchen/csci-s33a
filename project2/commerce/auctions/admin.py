from django.contrib import admin 

from .models import User, Listing, Category, Bid, Comment


class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'text', 'submitted')


class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user')


class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'amount', 'submitted')


admin.site.register(Listing, ListingAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category)
admin.site.register(User)