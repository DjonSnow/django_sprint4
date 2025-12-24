from django.contrib import admin
from .models import Category, Location, Post, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_editable = ('is_published',)
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'pub_date')
    list_editable = ('is_published',)
    list_filter = ('category', 'location')
    search_fields = ('title', 'text')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'author')
    list_editable = ('author',)
    search_fields = ('author',)


User = get_user_model()
try:
    admin.site.register(User, UserAdmin)
except admin.sites.AlreadyRegistered:
    pass
