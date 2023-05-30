from django.urls import path, include
from .views import CategoryListView, TagListView, CommentView, PostViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('comments', CommentView)



urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('tags/', TagListView.as_view()),
    # path('comments/', CommentListCreateView.as_view()),
    path('', include(router.urls))
    # path('posts/', PostViewSet.as_view({'get': 'list'})),
  



]