from django.urls import path

from . import views

app_name = 'tagging'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.index, name='index'),
    path('view_tags/<int:article_id>', views.view_tags, name='view_tags'),
    path('tag_article/<int:article_id>/<int:tag_id>', views.tag_article, name='tag_article'),
    path('landmark_papers', views.landmark_papers, name="landmark_papers"),
    path('mark_irrelevant/<int:article_id>', views.mark_irrelevant, name="mark_irrelevant"),
    path('export', views.export, name='export'),
    path('export_csv', views.export_csv, name='export_csv'),
    path('export_landmarks_csv', views.export_landmarks_csv, name='export_landmarks_csv'),
    path('export_mendeley', views.export_mendeley, name="export_mendeley")

    # path('process_article/<int:id>/<str:action>', views.process_article, name='process_article'),
]
