from rest_framework import viewsets
from .models import Post, Comment, Tag
from .serializers import PostSerializer, CommentSerializer, TagSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import FilterSet, filters

class PostFilter(FilterSet):
    tag=filters.NumberFilter(field_name='tags__id')
    class Meta:
        model = Post
        fields = ['tag']

class PostViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        qs = Post.objects.all().order_by('-created_at')
        tag_id = self.request.query_params.get('tag')
        if tag_id:
            qs = qs.filter(tags__id=tag_id)
        return qs
    

    serializer_class = PostSerializer
    filterset_class = PostFilter
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
# class tagViewSet -> /api/tags/
#                   -> /api/tags/3
# con login        -> /api/tags/ borrar o actualizar

# reto: crear un en-> filtro de lista de posts por tag
    
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    


     