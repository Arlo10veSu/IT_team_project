from django import forms
from django.contrib.auth.models import User

from rango.models import Category, Dish, UserProfile, UserComment


class CategoryForm(forms.ModelForm):
    category = forms.CharField(max_length=128,
                               help_text="Please tell me the category name.")
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('category',)


class DishForm(forms.ModelForm):
    dish = forms.CharField(max_length=128,
                           help_text="Please enter the dish name.")
    url = forms.CharField(
        help_text="Please enter the URL of dishes introduction.")
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    images = forms.CharField(widget=forms.HiddenInput(), initial="/static/images/photo.jpg", required=False)

    class Meta:
        model = Dish
        exclude = ('category',)


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class CommentForm(forms.ModelForm):
    likes = forms.BooleanField(required=False)
    comments = forms.CharField(label="多行输入", max_length=100, widget=forms.Textarea)

    #imge = forms.ImageField(label="图片上传")
    class Meta:
        model = UserComment
        fields = ('islike', 'comment')
