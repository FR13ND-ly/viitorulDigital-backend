from django.urls import path
from django.conf.urls import url
from . import views
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('user/login/', views.login),
    path('user/authorization/<str:token>/', views.getUserAuthorization),
    path('article/getArticle/<str:id>/', views.getArticle),
    path('article/getArticlesList/', views.getArticlesList),
    path('article/editArticle/', views.editArticle),
    path('article/like/', views.addLike),
    path('article/getLikes/', views.getLikesInfo),
    path('article/getComments/<int:id>/', views.getComments),
    path('article/addComment/', views.addComment),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT})
]