from django.db import models
import os
from django.utils.text import slugify
from django.contrib.auth.models import User

from PIL import Image

# Create your models here.
STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    cover_image = models.ImageField(upload_to="post_covers/", blank=True, null=True)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags = models.ManyToManyField("Tag", blank=True, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="posts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        if self.cover_image and os.path.isfile(self.cover_image.path):
            img = Image.open(self.cover_image.path)
            if img.height > 800 or img.width > 800:
                img.thumbnail((800, 800))
                img.save(self.cover_image.path)

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name