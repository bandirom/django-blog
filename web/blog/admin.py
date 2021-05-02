from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from .models import Article, Category, Comment


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'user', 'content')
    fields = ('author', 'user', 'content')


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'status', 'author')
    summernote_fields = ('content',)
    fields = ('category', 'title', 'status', 'author', 'image', 'content', 'created', 'updated')
    readonly_fields = ('created', 'updated')
    list_select_related = ('category', 'author', 'comment')
    list_filter = ('status',)
    inlines = (CommentsInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
