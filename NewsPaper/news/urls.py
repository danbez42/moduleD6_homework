from django.urls import path
from .views import PostsList, PostDetail, Test2, PostEdit, PostDelete, PostCreate, subscribe, warning

urlpatterns = [
    path('', PostsList.as_view(), name=''),
    path('category/<int:category_id>/', PostsList.as_view(), name='category_filter'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', Test2.as_view()),
    path('<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('<int:pk>/del/', PostDelete.as_view(), name='post_delete'),
    path('add/', PostCreate.as_view(), name ='post_create'),
    path('subscribe/', subscribe, name='subscribe'),
    path('warning/', warning, name = 'warning')
]