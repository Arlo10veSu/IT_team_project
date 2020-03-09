from django import forms
from django.contrib.auth.models import User

from rango.models import Category, Dish, UserProfile


class CategoryForm(forms.ModelForm):
   category = forms.CharField(max_length=128,
                          help_text="Please tell me the category name.")
   slug = forms.CharField(widget=forms.HiddenInput(), required=False)


   class Meta:
       model = Category
       fields = ('category', )


class DishForm(forms.ModelForm):
    dish = forms.CharField(max_length=128,
                            help_text="Please enter the dish name.")
    ingredient = forms.CharField(max_length=128,
                                 help_text="Please enter the ingredients.")
    cost = forms.CharField(max_length=128,
                           help_text="Please tell me the price of the dishes")
    url = forms.URLField(max_length=200,
                         help_text="Please enter the URL of dishes introduction.")

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startwith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url
        return cleaned_data

    class Meta:
        model = Dish
        exclude = ('category', )


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture')

