from django.contrib import admin
from .views import Article, Comment, Like, Profile

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Profile)
