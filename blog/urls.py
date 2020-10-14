from django.urls import path
from .views import PostList, post_detail, CreatePost, PostDelete, PostUpdate, CategoryView, TagListView
from accounts.views import folder, FolderDeleteView, Rename, PhotoUploadView

app_name = "blog"

urlpatterns = [
    path('', PostList, name='home'),
    path('detail/<str:slug>/<int:my_num>/',post_detail, name='postdetail'),
    path('add_post', CreatePost.as_view(), name='new_post'),
    path('delete/<int:pk>', PostDelete.as_view(), name='delete'),
    path('update/<int:pk>', PostUpdate.as_view(), name='update'),
    path('category/<int:category_slug>/', CategoryView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', TagListView.as_view(), name='post_list_by_tag'),
    path('folder/<int:folder_field>/', folder, name='folder'),
    path('folder/delete/<int:pk>', FolderDeleteView.as_view(), name='delete_folder'),
    path('folder/update/<int:pk>', Rename.as_view(), name='folder_rename'),
    path('picture/<int:folder_id>/', PhotoUploadView, name='photo_upload')
]                                          