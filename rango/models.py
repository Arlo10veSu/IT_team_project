from django.db import models

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
    ingredient = models.CharField(max_length=128,)
    cost = models.CharField(max_length=128)
    url = models.URLField()

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return self.dish

