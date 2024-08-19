from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .import views

app_name = 'polls'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('home/', views.home, name='home'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)