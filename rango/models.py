from django.contrib.auth.models import User
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
    url = models.URLField()
    likes = models.IntegerField(default=0)

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


class RemarkForm(forms.Form):
    subject = forms.CharField(max_length=100,label='Mark Board')
    mail = forms.EmailField(label='email')
    topic = forms.ChoiceField(choices=TOPIC_CHOICES,label='choose one topic')
    message = forms.CharField(label='content for mark',widget=forms.Textarea)
    cc_myself = forms.BooleanField(required=False,label='watch this tie')


class Remark(models.Model):
    subject = models.CharField(max_length=100)
    mail = models.EmailField()
    topic = models.CharField(max_length=100)
    message = models.CharField(max_length=300)
    cc_myself = models.BooleanField()

    def __str__(self):
        return self.subject

    class Meta:
        ordering = ['subject']


class UserInfor(models.Model):
    username = models.CharField(max_length=64)
    comment = models.CharField(max_length=1028, default='')

    def __str__(self):
        return self.username