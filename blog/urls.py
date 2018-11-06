from django.conf.urls import include, url
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('new/', views.post_new, name='post_new'),
    path('<pk>/', views.post_detail, name='post_detail'),
    path('<pk>/edit/', views.post_edit, name='post_edit'),
    path('<pk>/delete/', views.post_delete, name='post_delete'),
    path('<pk>/like/', views.post_like, name='post_like'),


    path('<post_pk>/comments/', views.comment_list, name='comment_list'),
    path('<post_pk>/comments/new/', views.comment_new, name='comment_new'),
    path('<post_pk>/comments/<pk>/edit/', views.comment_edit, name='comment_edit'),
    path('<post_pk>/comments/<pk>/delete/', views.comment_delete, name='comment_delete'),
    path('comments/<pk>/like/', views.comment_like, name='comment_like'),

    url('^posts\.json$', views.post_list_json),
    url('^api/v1/', include('blog.api')),
    # path('posts\.json', views.post_list_json),
    # path('api/v1/', include('blog.api')),
]








