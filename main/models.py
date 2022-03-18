from django.db import models
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image


def get_unique_id(model, post=True):
    random_string = slugify(get_random_string(10))
    if post:
        while model.posts.filter(no=random_string).exists():
            random_string = slugify(get_random_string(10))
    else:
        while model.comments.filter(no=random_string).exists():
            random_string = slugify(get_random_string(10))
    return random_string


class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    banner = models.ImageField(upload_to="banners")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("main:board", args=[self.name])


class Post(models.Model):
    name = models.CharField(max_length=30, blank=True)
    title = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to="post_images")
    no = models.SlugField(max_length=10, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(default=timezone.now)
    board = models.ForeignKey(Board, on_delete=models.CASCADE,
                              related_name="posts")

    class Meta:
        ordering = ["-last_activity"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("main:post", args=[self.board.name, self.no])

    def save(self, *args, **kwargs):
        if not self.no:
            self.no = get_unique_id(self.board)
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 600:
            out_size = (500, 600)
            img.thumbnail(out_size)
            img.save(self.image.path)


class Comment(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to="comment_images", blank=True)
    no = models.SlugField(max_length=10, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name="comments")
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True,
                               blank=True, related_name="replies")

    class Meta:
        ordering = ["created"]
        get_latest_by = 'created'

    def save(self, *args, **kwargs):
        if not self.no:
            self.no = get_unique_id(self.post, post=False)
            self.post.last_activity = timezone.now()
            self.post.save()
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.height > 500 or img.width > 600:
                out_size = (500, 600)
                img.thumbnail(out_size)
                img.save(self.image.path)