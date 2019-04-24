from django import forms
from .models import DataModel
from django.forms import ModelForm



class DForm(ModelForm):
    class Meta:
        model = DataModel
        fields=['fname','lname','email','address','country','zipcode','data']
        widgets = {
            "fname": forms.TextInput(attrs={"class":"form-control","placeholder":"First Name"}),
            "lname": forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name"}),
            "email": forms.TextInput(attrs={"class":"form-control","placeholder":"Email Id"}),
            "address":forms.TextInput(attrs={"class":"form-control","placeholder":"Address 1"}),
            "country": forms.Select(attrs={"class":"custom-select d-block w-100"}),
            "zipcode": forms.NumberInput(attrs={"class":"form-control","placeholder":"Zipcode"}),
            "data": forms.Textarea(attrs={"class":"form-control","cursor":"inherit"})
        }

"""
class DataForm(forms.Form):
    fname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),label='First Name', max_length=25,required=True,)
    lname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),label='Last Name',max_length=25,required=True)
    email = forms.EmailField(widget=forms.TextInput(attrs={"class":"form-control"}),label='Email',required=True,)
    address = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}),label='Address',max_length=1000)
    country = forms.ChoiceField(widget=forms.Select(attrs={"class":"custom-select d-block w-100",}),choices=(('Option 1','United States'),('Option 2','India')),)
    zipcode = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control"}),label='Zip')
    data = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","cursor":"inherit"}),max_length=2000)
"""

class LoginForm(forms.Form):
    email = forms.EmailField(label='Email Address',required=True)
    password = forms.PasswordInput()
