from django.contrib import admin
from screening.models import *
# Register your models here.

@admin.register(PubmedImport)
class PubmedImportAdmin(admin.ModelAdmin):
    list_display = ['import_date', 'search_function']


@admin.register(PubmedImportedArticle)
class PubmedImportedArticleAdmin(admin.ModelAdmin):
    list_display = ['pmid', 'pub_date', 'title', 'authors', 'pubmed_url']


admin.site.register(Highlight)
admin.site.register(ScreeningStatus)
