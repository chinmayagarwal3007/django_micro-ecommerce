from django.urls import path # type: ignore
from . import views

app_name = 'products'
urlpatterns = [
    path('create/', views.product_create_view, name='create'),
    path('', views.product_list_view, name='list'),
    path('<slug:slug>/', views.product_detail_view, name='detail'),\
    path('<slug:slug>/download', views.product_attachment_download_view, name='download'),
]
