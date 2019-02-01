from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('comment/<int:post_pk>/', views.comment_create, name='comment_create'),
    path('reply/<int:comment_pk>/', views.reply_create, name='reply_create'),
]
