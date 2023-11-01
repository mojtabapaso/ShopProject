from django import forms
from products.models import Brand
from django.forms import ModelForm, CheckboxInput


class SearchForm(forms.Form):
    search = forms.CharField(label='')


class FilterForm(forms.Form):
    filter_min = forms.CharField()
    filter_max = forms.CharField()


# brand = Brand.objects.all()
# print(brand)
# for i in brand:
#     print(i.slug)
#
#
# class FilterBrand(forms.Form):
#     for i in brand:
#         i.slug = forms.CharField(widget=CheckboxInput())
#     name = forms.CharField(widget=CheckboxInput())