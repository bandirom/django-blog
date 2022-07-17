from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Article, Category, Comment


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'status', 'author')
    summernote_fields = ('content',)
    fields = ('category', 'title', 'status', 'author', 'image', 'content', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    list_select_related = ('category', 'author')
    list_filter = ('status',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
