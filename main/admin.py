from django.contrib import admin
from .models import Board, Post, Comment

admin.site.site_header = "Chan Admin Panel"


class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'banner')


class PostAdmin(admin.ModelAdmin):
    list_filter = ('created', 'last_activity')


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('created',)


admin.site.register(Board, BoardAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
