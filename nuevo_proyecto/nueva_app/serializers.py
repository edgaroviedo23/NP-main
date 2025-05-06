from rest_framework import serializers
from .models import Post, Comment, Tag

class TagSerializer(serializers.ModelSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Tag
        fields = ['id', 'name', 'posts']


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)


    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'tags'] 

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at']


    