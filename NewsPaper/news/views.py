from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DetailView, DeleteView
# from django.views import View
from django.core.paginator import Paginator

from .models import *
from .filters import NewsFilter
from .forms import NewsForm


class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        # context['categories'] = Category.objects.all()
        # context['form'] = NewsForm()
        return context

    # def post(self, request, *args, **kwargs):
    #   form = self.form_class(request.POST)
    #   if form.is_valid():
    #       form.save()
    #   return super().get(request, *args, **kwargs)


class NewsSearch(ListView):
    model = Post
    template_name = 'news_filter.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewsFilter(self.request.GET, queryset=self.get_queryset())
        return context


# class NewsDetail(DetailView):
#   model = Post
#   template_name = 'post.html'
#   context_object_name = 'post'


class NewsDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()


class NewsCreateView(CreateView):
    template_name = 'news_add.html'
    form_class = NewsForm


class NewsUpdateView(UpdateView):
    template_name = 'news_edit.html'
    form_class = NewsForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class NewsDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'