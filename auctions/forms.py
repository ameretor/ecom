from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets
from .models import listing, Gender, User, category


class Add_listing(forms.ModelForm):
    class Meta:
        model = listing
        fields = ('title', 'description', 'stock',
                  'category', 'sex', 'end_date', 'image')
        widgets = {'title': forms.TextInput(
            attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'category': forms.Select(choices=(category.objects.all()), attrs={'class': 'form-control'}),
            'sex': forms.Select(choices=(Gender.objects.all()), attrs={'class': 'form-control'}),
            'end_date': forms.SelectDateWidget(empty_label=(" Choose Year ", " Choose Month ", " Choose Day "))
        }
    latest_bid = forms.DecimalField(
        label='Latest bid $', max_digits=9, decimal_places=2)
