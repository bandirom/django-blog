from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from actions.admin import LikeDislikeInline

from .forms import ArticleForm
from .models import Article, ArticleTag, Category, Comment


class CommentsInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('author', 'user', 'content')
    fields = ('author', 'user', 'content')


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fields = ('name',)


@admin.register(Article)
class ArticleAdmin(SummernoteModelAdmin):
    form = ArticleForm
    list_display = ('title', 'category', 'status', 'author', 'tag_list_str')
    summernote_fields = ('content',)
    fields = ('category', 'title', 'status', 'author', 'image', 'content', 'created', 'updated', 'tags')
    readonly_fields = ('created', 'updated')
    list_select_related = ('category', 'author')
    list_filter = ('status',)
    inlines = (CommentsInline, LikeDislikeInline)
    save_as = True
    list_editable = ('status', 'author')
    filter_horizontal = ('tags',)

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('comment_set', 'tags')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ('name',)
