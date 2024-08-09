from django.contrib import admin

from .models import User, Game, GamePlayer, Board


class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'creator', 'started', 'numplayers')

class GamePlayerAdmin(admin.ModelAdmin):
    list_display = ('game', 'user')
    
admin.site.register(User)
admin.site.register(Board)
admin.site.register(Game, GameAdmin)
admin.site.register(GamePlayer, GamePlayerAdmin)
