from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from .models import Post, Category, Subscribers
from .filters import PostFilter
from django_filters.views import FilterView
from django.contrib.auth.decorators import login_required
from .forms import NewsEditForm, NewsAddForm
from django.utils import timezone
from django.http import HttpResponseRedirect

# Create your views here.
class PostsList(ListView):
    model = Post
    template_name ='news.html'
    context_object_name = 'news'
    paginate_by = 10
    def get_queryset(self):
        if len(self.kwargs):
            category = Category.objects.get(id=self.kwargs['category_id'])
            queryset = Post.objects.filter(categories=category).order_by('-time_create')
        else:
            queryset = Post.objects.order_by('-time_create')
        return queryset
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(**kwargs)
        context['is_author'] = user.groups.filter(name = 'Authors').exists()
        context['categories'] = Category.objects.all()

        if len(self.kwargs):
            context['category_name'] = Category.objects.get(id=self.kwargs['category_id'])
            if user.is_authenticated:
                context['user_subsсribed'] = user.subscribers_set.filter(news_category__new_category=context['category_name'])
        return context


class PostDetail(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name = 'Authors').exists()
        return context

class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news_edit.html'
    form_class = NewsEditForm
    permission_required = ('news.change_post',)

class Test2(FilterView):
    model = Post
    context_object_name = 'search'
    template_name = 'search.html'
    filterset_class = PostFilter

class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('')
    permission_required = 'news.delete_post'

class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news_add.html'
    form_class = NewsAddForm
    permission_required = 'news.add_post'


    def form_valid(self, form):
        self.object = form.save(commit=False)
        user_posts_count = Post.objects.filter(author=self.object.author,
                                               time_create__date=timezone.now().date()).count()
        if user_posts_count >= 3:
            return HttpResponseRedirect(reverse('warning'))
        self.object.save()
        form.save_m2m()
        return super().form_valid(form)
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user'] = self.request.user
        return kwargs


@login_required
def subscribe(request):
    user = request.user
    category = Category.objects.get(new_category=request.GET.get('category_name'))
    if not Subscribers.objects.filter(user=user).exists():
        new_subscriber = Subscribers.objects.create(user=user)
        category.subscribers_set.add(new_subscriber)
    else:
        obj_subscribe = Subscribers.objects.get(user=user)
        category.subscribers_set.add(obj_subscribe)

    return redirect('/news/category/' + str(category.pk))

def warning(request):
    user = request.user
    context = {'username': user.username}
    return render(request, 'warning.html', context)