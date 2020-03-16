from django import forms
from django.contrib.auth.models import User

from app_shop.models import Category, Product, Basket, Comment


class AddCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['votes', 'added_date']


class AddProductToBasketForm(forms.Form):
    product = forms.IntegerField()


class RemoveCategoryForm(forms.Form):
    category = forms.IntegerField()


class AddCommentForm(forms.Form):
    product = forms.IntegerField()
    customer = forms.IntegerField()
    text = forms.Textarea()