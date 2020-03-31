from django.contrib import admin
from tagging.models import *
# Register your models here.

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'tag_name', 'tag_group']


@admin.register(ArticleTag)
class ArticleTagAdmin(admin.ModelAdmin):
    list_display = ['id', 'article', 'tag']


@admin.register(TagGroup)
class TagGroupAdmin(admin.ModelAdmin):
    list_display = ['id', 'group_name', 'enabled']

@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ['id', 'keyword', 'css_class']
