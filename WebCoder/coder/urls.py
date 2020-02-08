from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('UploadFile/', views.upload_file, name='UploadFile'),
    path('ProjectView/', views.project_view, name='ProjectView'),
    path('TransCode/', views.trans_code, name='TransCode'),
    path('DownloadFile/', views.download_file, name='DownloadFile'),
]
