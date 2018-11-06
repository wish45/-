from django.db import models
from django.urls import reverse
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self): #
        return reverse('blog:post_detail', args=[self.pk])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,) #on_delete=models.CASCADE, 추가해줬다.
    message = models.TextField()
    photo = models.ImageField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_count = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    class Meta:
        ordering = ['-id']

# 1:1 원투원
# 1:다 외래키
# 다대다 매니투매니층






