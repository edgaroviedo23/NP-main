from rest_framework import routers
from .api_views import PostViewSet, CommentViewSet, TagViewSet

router = routers.DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')

router.register(r'comments', CommentViewSet, basename='comment')

router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = router.urls