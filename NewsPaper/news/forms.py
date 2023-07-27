from django.forms import ModelForm
from .models import Post, Category, Author

class NewsEditForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text']

class NewsAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user')
        super(NewsAddForm, self).__init__(*args, **kwargs)
        self.fields['author'].queryset = Author.objects.filter(author=self.current_user)
        self.fields['author'].initial = Author.objects.get(author=self.current_user)
        self.fields['author'].disabled = True

    categories = Category.objects.all()
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories', 'author']