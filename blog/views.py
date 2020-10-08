from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView, View
from .models import Post, Comment, Reply, Category, Subscribe
from .forms import CommentForm, ReplyForm, PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from .forms import SearchForm, SubscribingForm
from .models import PostView
from django.contrib import messages
import os
# from django.contrib import messages TODO: display a message when the user succesfully upload a new post
# Create your views here.


class CreatePost(UserPassesTestMixin, CreateView):
    """this is a class that will render a form containing title, body, author and time
    the post was published upon submission a newly post appear on the list of posts page."""
    form_class = PostForm  #
    template_name = 'add_post.html'   # this is the page name that the form will display
    success_url = '/blog/' #  this is the url of the page you will  be take after submitting the form
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreatePost, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_staff


def PostList(request):
    post = Post.objects.all()
    form = SearchForm
    results = []
    query = None
    subscribingform = SubscribingForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query =  SearchQuery(query)
            results = Post.objects.annotate(
                search=search_vector,
                rank = SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
    if request.method == 'POST':
        subscribingform = SubscribingForm(request.POST)
        if subscribingform.is_valid():
            check_it = Subscribe.objects.filter(email=subscribingform.instance.email)
            if check_it.exists():
                messages.info(request, 'You are Already Subscribed')
                subscribingform = SubscribingForm()
            else:
                subscribingform.save()
                messages.success(request, 'you are subscribed succssifully!')
                subscribingform = SubscribingForm()
    return render(request, 'post_list.html', {'post':post, 'search_form':form, 'query':query, 
    'results': results, 'subscribingform': subscribingform})


def post_detail(request, slug,  my_num):
    user = request.user          
    post = get_object_or_404(Post, id=my_num)
    form = CommentForm()
    if request.user.is_authenticated:
        PostView.objects.get_or_create(user=user, post=post)
    if 'comment' in request.GET:
        form = CommentForm(request.GET)
        if form.is_valid():
            check_it = Comment.objects.filter(comment=form.instance.comment, name=user)
            if check_it.exists():
                form = CommentForm()
            else:
                comment = form.cleaned_data['comment']
                post.comment_set.create(comment=comment, post=post, name=user)
                form = CommentForm()
    return render(request, 'post_detail.html', {'object': post, 'user': user, 'form': form})
    
# def view(request):
#     ...
#     cookie_state = request.COOKIES.get('viewed_post_%s' % post_name_slug)
#     response = render_to_response('community/post.html',context_instance=RequestContext(request, context_dict))
#     if cookie_state:
#         Post.objects.filter(id=post.id).update(total_views=F('total_views') + 1)
#     else:
#         Post.objects.filter(id=post.id).update(unique_views=F('unique_views') + 1)
#         Post.objects.filter(id=post.id).update(total_views=F('total_views') + 1)
#                         response.set_cookie('viewed_post_%s' % post_name_slug , True, max_age=2678400)
#     return response



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
    fields = ['post_picture', 'title', 'body',]

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(PostUpdate, self).form_valid(form)
    

class PostDelete(UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('blog:home')  # this is the name of the url to be displayed when a post
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
                    search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
                    search_query =  SearchQuery(query)
                    results = Post.objects.annotate(
                search=search_vector,
                rank = SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')
            return render(request, 'category.html', {'category': category, 'post': post, 'search_form':form, 'query':query, 
    'results': results})



def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def error_403_view(request, exception):
    return render(request, '403.html', status=403)

def error_500_view(request, exception):
    return render(request, '500.html', status=500)