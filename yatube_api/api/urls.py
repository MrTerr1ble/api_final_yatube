from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)
router.register('follow', FollowViewSet)

comment_router = NestedDefaultRouter(router, 'posts', lookup='post')
comment_router.register('comments', CommentViewSet)

urlpatterns = [
    path('', include('djoser.urls.jwt')),
    path('', include(router.urls)),
    path('', include(comment_router.urls))
]
