from django.contrib import admin
from .models import Post, Comment, Reply, Category, PostPicture, Folder, Subscribe
# Register your models here.
class CommentInline(admin.StackedInline):
    model = Comment

class ReplyAdmin(admin.TabularInline):
    model = Reply

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'publish', 'status']
    list_filter = ['publish', 'author']
    search_fields = ['title', 'body',]
    inlines = [CommentInline]
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    inlines = [ReplyAdmin]

admin.site.register(Category)
admin.site.register(PostPicture)
admin.site.register(Folder)
admin.site.register(Subscribe)