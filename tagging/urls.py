from django.urls import path

from . import views

app_name = 'tagging'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.index, name='index'),
    path('tag_article/<int:article_id>/<int:tag_id>', views.tag_article, name='tag_article'),
    path('export', views.export, name='export'),
    path('export_csv', views.export_csv, name='export_csv'),
    path('export_mendeley', views.export_mendeley, name="export_mendeley")

    # path('process_article/<int:id>/<str:action>', views.process_article, name='process_article'),
]
