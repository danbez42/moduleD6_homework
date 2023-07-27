from django.contrib import admin
from .models import Post, Subscribers, PostCategory, Author
# Register your models here.

class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    extra = 1

class PostAdmin(admin.ModelAdmin):
    inlines = (PostCategoryInLine,)

admin.site.register(Post, PostAdmin)
admin.site.register(Subscribers)
admin.site.register(Author)
