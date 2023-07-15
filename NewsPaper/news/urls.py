from django.urls import path
from .views import NewsList, NewsSearch, NewsDetailView, NewsCreateView, NewsUpdateView, NewsDeleteView

urlpatterns = [
  path('', NewsList.as_view()),
  # path('<int:pk>', NewsDetail.as_view()),
  path('search/', NewsSearch.as_view()),
  path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
  path('<int:pk>/edit', NewsUpdateView.as_view(), name='news_edit'),
  path('add/', NewsCreateView.as_view(), name='news_add'),
  path('<int:pk>/delete', NewsDeleteView.as_view(), name='news_delete'),
]