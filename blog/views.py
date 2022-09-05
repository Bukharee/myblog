from unicodedata import category
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, CreateView, View
from .models import Post, Comment, Category, Subscribe
from .forms import CommentForm,  PostForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from .forms import SearchForm, SubscribingForm
from django.contrib import messages
from itertools import groupby
from operator import attrgetter
# from django.contrib import messages TODO: display a message when the user succesfully upload a new post
# Create your views here.


class CreatePost(UserPassesTestMixin, CreateView):
    """this is a class that will render a form containing title, body, author and time
    the post was published upon submission a newly post appear on the list of posts page."""
    form_class = PostForm  #
    # this is the page name that the form will display
    template_name = 'add_post.html'
    success_url = '/'  # this is the url of the page you will  be take after submitting the form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePost, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


def PostList(request):
    top_posts = Post.objects.order_by('-views')[:5]
    post = Post.objects.all().order_by('-views')
    posts = groupby(post, key=attrgetter('category'))
    grouped_posts = {}
    form = SearchForm
    results = []
    query = None
    subscribingform = SubscribingForm()
    for category, posts in posts:
        print(category)
        for p in posts:
            if category in grouped_posts:
                if len(grouped_posts[category]) < 3:
                    grouped_posts[category].append(p)
                    print(p)
            else:
                grouped_posts[category] = [p]
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector(
                'title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)
            results = Post.objects.annotate(
                search=search_vector,
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    if request.method == 'POST':
        subscribingform = SubscribingForm(request.POST)
        if subscribingform.is_valid():
            check_it = Subscribe.objects.filter(
                email=subscribingform.instance.email)
            if check_it.exists():
                messages.info(request, 'You are Already Subscribed')
                subscribingform = SubscribingForm()
            else:
                subscribingform.save()
                messages.success(request, 'you are subscribed succssifully!')
                subscribingform = SubscribingForm()
    return render(request, 'post_list.html', {'post': grouped_posts, 'top_posts': top_posts, 'search_form': form, 'query': query,
                                              'results': results, 'subscribingform': subscribingform})


def post_detail(request, slug):
    user = request.user
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    print(post.title)
    form = CommentForm()
    if 'comment' in request.GET:
        form = CommentForm(request.GET)
        if form.is_valid():
            check_it = Comment.objects.filter(
                comment=form.instance.comment, name=user)
            if check_it.exists():
                form = CommentForm()
            else:
                comment = form.cleaned_data['comment']
                post.comment_set.create(comment=comment, post=post, name=user)
                form = CommentForm()
    return render(request, 'post_detail.html', {'object': post, 'user': user, 'form': form})


class TagListView(ListView):
    def get(self, request, tag_slug=None):
        tag = None
        post = Post.objects.all()

        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            post = Post.objects.filter(tags__in=[tag])
        return render(request, 'tags.html', {'tag': tag, 'post': post})


class PostUpdate(UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['post_picture', 'title', 'body', ]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdate, self).form_valid(form)


class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    # this is the name of the url to be displayed when a post
    success_url = reverse_lazy('blog:home')
    # is successifully deleted

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user


class CategoryView(ListView):
    def get(self, request, category_slug=None):
        category = None
        post = Post.objects.all()
        form = SearchForm
        results = []
        query = None
        if category_slug:
            category = get_object_or_404(Category, id=category_slug)
            post = Post.objects.filter(category=category)
            if 'query' in request.GET:
                form = SearchForm(request.GET)
                if form.is_valid():
                    query = form.cleaned_data['query']
                    search_vector = SearchVector(
                        'title', weight='A') + SearchVector('body', weight='B')
                    search_query = SearchQuery(query)
                    results = Post.objects.annotate(
                        search=search_vector,
                        rank=SearchRank(search_vector, search_query)
                    ).filter(rank__gte=0.3).order_by('-rank')
            return render(request, 'category.html', {'category': category, 'post': post, 'search_form': form, 'query': query,
                                                     'results': results})


def error_404_view(request, exception):
    return render(request, '404.html', status=404)


def error_403_view(request, exception):
    return render(request, '403.html', status=403)


def error_500_view(request, exception):
    return render(request, '500.html', status=500)
