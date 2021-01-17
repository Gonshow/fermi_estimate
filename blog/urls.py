from django.urls import path,include
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.PostList.as_view(), name='post_list'),
    path('detail/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('create/',views.PostCreate.as_view(), name='post_create'),
    path('delete/<pk>',views.PostDelete.as_view(),name='post_delete'),
    path('comment/<int:post_pk>/', views.comment_create, name='comment_create'),
    path('reply/<int:comment_pk>/', views.reply_create, name='reply_create'),
    path('update/<post_pk>', views.post_update, name="post_update"),
    path('detail/<post_pk>/<comment_pk>/formulation', views.comment_update, name='comment_update'),
    path('detail/<post_pk>/<comment_pk>/quantify/', views.comment_update_num, name='add_value'),
    #path('detail/quantify/', views.AddValue.as_view(), name='add_value'),
]
