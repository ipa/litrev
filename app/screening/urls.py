from django.urls import path

from . import views

app_name = 'screening'
urlpatterns = [
    path('', views.index, name='index'),
    path('process_article/<int:id>/<str:action>', views.process_article, name='process_article'),
    path('import_pubmedids_view/', views.import_pubmedids_view, name='import_pubmedids_view')
]
