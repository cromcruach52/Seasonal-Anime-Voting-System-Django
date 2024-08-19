from django.urls import path
from . import views

app_name = 'voteStatistics'

urlpatterns = [
    path('', views.vote_statistics, name='vote_statistics'),
    path('category_statistics/', views.category_statistics, name='category_statistics'),  # Add a named pattern for your view
]
