from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager
# Create your models here.
from django.contrib.postgres.search import SearchVector


class Category(models.Model):
    category = models.CharField(max_length=200)

    def __str__(self):
        return self.category


class Comment(models.Model):
    name = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return self.comment
    
    @staticmethod
    def get_absolute_url():
        return reverse('blog:home', args=[])


class PostView(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)


class Post(models.Model):
    STATUS_CHOICES = (('published', 'Published'), ('draft', 'Draft'))
    post_picture = models.ImageField(upload_to='post/%Y/%m/%d', null=True,)
    title = models.CharField(max_length=225)
    body = models.TextField()
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    publish = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField()
    created = models.DateTimeField(default=timezone.now())
    updated = models.DateTimeField(default=timezone.now())
    status = models.CharField(choices=STATUS_CHOICES, default='draft', max_length=20)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    next_post = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)
    previous_post = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    tags = TaggableManager()
    content = models.CharField(blank=True, null=True, max_length=200);
    search_vector = SearchVector()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        return reverse('blog:postdetail', args=[str(self.title).replace(' ', '-').lower(), self.id, ])

    def get_tag(self):
        return reverse('blog:post_list_tag', args=[self.tags.slug, ])

    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

    def get_updated(self):
        return reverse('blog:update', args=[self.id])

    def get_deleted(self):
        return reverse('blog:delete', args=[self.id])


class Reply(models.Model):
    name = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    reply = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField(default='i really wanna reply')

    def __str__(self):
        return self.reply

    def get_absolute_url(self):
        pass


class PostPicture(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='postimage/%Y/%m/%d')
    search_vector = SearchVector()
    timestamp = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey('Folder', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Folder(models.Model):
    name = models.CharField(max_length=10)
    search_vector = SearchVector()
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:folder', args=[self.id])

    def get_deleted(self):
        return reverse('blog:delete_folder', args=[self.id])

    def get_renamed(self):
        return reverse('blog:folder_rename', args=[self.id])

    def save_in_folder(self):
        return reverse('blog:photo_upload', args=[self.id])


class Subscribe(models.Model):
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True)
