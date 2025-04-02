from django.urls import path
from . import views


app_name = 'resources'
urlpatterns = [
    path('', views.ResourceListView.as_view(), name='resource-list'),
    path('<str:slug>/', views.ResourceDetailView.as_view(), name='resource-detail'),
    path('api/resource/<int:pk>/watermarked/', views.WatermarkedFileView.as_view(), name='watermarked-file'),
    path('api/resource/<int:pk>/download/', views.DownloadFileView.as_view(), name='download-file'),
    path('home_resourses/', views.HomePageView.as_view(), name='home_resourse'),
    # path('category_resources/<int:id>/', views.CategoryRecoursesView.as_view(), name='category_resurslari'),
    # path('resource_type/<int:id>/', views.ResourceTypeResourcesView.as_view(), name='resource-type')
       
]

from django.shortcuts import render
from django.http import Http404

def my_view(request):
    raise Http404  

def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


handler404 = "apps.resources.views.custom_404_view"