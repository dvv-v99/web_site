from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.home, name='home'),
    
    
    path('projects/', views.ProjectsView.as_view(), name='projects'),
    
     
    path('news/', views.PostView.as_view(), name='news'),
    
   
    path('about/', views.AboutView.as_view(), name='about'),
    
]