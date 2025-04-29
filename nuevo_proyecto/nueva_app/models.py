from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', related_name="post_tags", blank=True)  # Cambié related_name

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50)
    posts = models.ManyToManyField('Post', related_name="tag_posts", blank=True)  # Cambié related_name

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentario por {self.author.username} en {self.post.title}"
