from django import forms
from .models import Product
from ckeditor.fields import RichTextField
from .models import ProductComment
from Account.models import Address

class LoginForm(forms.Form):
    username = forms.CharField(max_length=120, label="Username", label_suffix="")
    password = forms.CharField(max_length=120, widget=forms.PasswordInput, label="Password", label_suffix="")


class CustomerRegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label_suffix="")
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, label_suffix="")

    name = forms.CharField(max_length=100, label_suffix="")
    lastName = forms.CharField(max_length=100, label_suffix="")
    email = forms.EmailField(label_suffix="")


class ShopRegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label_suffix="")
    password = forms.CharField(widget=forms.PasswordInput, max_length=100, label_suffix="")

    shopName = forms.CharField(max_length=80, label_suffix="")
    addres = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField(label_suffix="")



class NewProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['Name', 'Price', 'Description', 'Category', 'Brand', "Photo1", "Photo2", "Photo3", "Photo4", "Photo5",]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"