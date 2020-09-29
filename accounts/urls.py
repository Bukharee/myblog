from django.urls import path
from .views import SignUpView, Update, edit_user, Dashboard, FolderCreateView, FolderDeleteView, Rename, get_his_profile

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('update/<int:pk>',Update.as_view(), name='update'),
    path('edit/', edit_user, name='edit'),
    path('dashboard/', Dashboard, name='dash'),
    path('folder/', FolderCreateView.as_view(), name='create_folder'),
    path('get_profile/<int:his_id>', get_his_profile, name='get_profile')

]