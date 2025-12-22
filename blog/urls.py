from django.urls import path
from blog import views
from blog.views import PostDetailView

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
]
