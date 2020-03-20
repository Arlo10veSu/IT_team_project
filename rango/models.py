from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django import forms

# Create your models here.
from django.template.defaultfilters import slugify


class Category(models.Model):
    category = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        self.slug = slugify(self.category)
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category


class Dish(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    dish = models.CharField(max_length=128, unique=True)
    url = models.CharField(max_length=128, default="https://www.allrecipes.com/recipes/1642/everyday-cooking/")
    likes = models.IntegerField(default=0)
    images = models.CharField(max_length=128, default="/static/images/photo.jpg")

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return self.dish


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


TOPIC_CHOICES = (
    ('level1', 'Bad'),
    ('level2', 'Soso'),
    ('level3', 'Good'),
)


class UserComment(models.Model):
    username = models.CharField(max_length=64)
    comment = models.CharField(max_length=1028, default='')
    dish = models.CharField(max_length=128, default='')
    islike = models.BooleanField(default=True)

    def __str__(self):
        return self.username

