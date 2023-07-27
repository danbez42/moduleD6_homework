from django import forms

from .models import Post
from django_filters import FilterSet, DateFilter, CharFilter

class PostFilter(FilterSet):
    time_create = DateFilter(widget=forms.DateInput(attrs={'type':'date'}),
                                            lookup_expr='gt')
    title = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Post
        fields = ('author',)