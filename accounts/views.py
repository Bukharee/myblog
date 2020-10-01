from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserCreationForm, CustomUserChangeForm
from django.contrib.auth  import get_user_model
from .forms import UserEditForm, CreateFolderForm, PhotoUploadForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from blog.models import Post, PostPicture, Folder
from blog.forms import SearchForm
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Folder, PostPicture
from django.urls import reverse
# Create your views here.

class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name  = 'signup.html'

class Update(generic.UpdateView):
    model = get_user_model()
    success_url = reverse_lazy('blog:home')
    template_name = 'profile.html'

def edit_user(request):
    user = request.user
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('blog:home')
    else:
        form = UserEditForm(instance=user)
    return render(request, 'profile_edit.html', {'form': form})
    
@login_required
def Dashboard(request):
    user = request.user
    post = Post.objects.filter(author=user)
    folder = Folder.objects.filter(user=user)
    form = SearchForm
    query = None
    results = []
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
    return render(request, 'profile.html', {'user': user, 'post': post, 'search_form':form, 'query':query, 'results': results, 'folder': folder})

def folder(request, folder_field=None):
    folder = get_object_or_404(Folder, id=folder_field)
    user = request.user
    images = PostPicture.objects.filter(folder=folder_field, user=user)
    return render(request, 'folder.html', {'folder': folder, 'images': images})

class FolderCreateView(UserPassesTestMixin, CreateView):
    form_class = CreateFolderForm
    template_name = 'create_folder.html'
    success_url = '/blog/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(FolderCreateView, self).form_valid(form)

    def test_func(self):
        return self.request.user.is_staff

class FolderDeleteView(UserPassesTestMixin, DeleteView):
    model = Folder
    fields = ['name',]
    template_name = 'folder_delete.html'
    success_url = reverse_lazy('account:dash')

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

class Rename(UserPassesTestMixin, UpdateView):
    model = Folder
    fields = ('name', )
    template_name = 'folder_rename.html'

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user

def PhotoUploadView(request, folder_id):
    form = PhotoUploadForm()
    folder = get_object_or_404(Folder, id=folder_id)
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.folder = folder
            new_form.user = request.user
            new_form.save()
            return redirect(reverse('blog:photo_upload', args=[folder_id]))
    return render(request, 'upload_photo.html', {'form': form})

        

def get_his_profile(request, his_id):
    user = get_object_or_404(get_user_model(), id=his_id)
    post = Post.objects.filter(author=user)
    return render(request, 'normal_user_profile.html', {'user': user, 'post': post})