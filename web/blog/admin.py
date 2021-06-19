from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from actions.admin import LikeDislikeInline
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
    list_select_related = ('category', 'author')
    list_filter = ('status',)
    inlines = (CommentsInline, LikeDislikeInline)
    save_as = True
    list_editable = ('status', 'author')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comment_set')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
