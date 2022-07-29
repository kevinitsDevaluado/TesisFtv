from datetime import datetime

from django import forms

from core.clinic.choices import *
from core.clinic.models import Mascots, ProductType, BreedPet
from core.reports.choices import months


class ReportForm(forms.Form):
    year = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control datetimepicker-input',
        'data-toggle': 'datetimepicker',
        'data-target': '#year',
    }))

    month = forms.ChoiceField(choices=months, widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    date_joined = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'date_joined',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#date_joined'
        }))

    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    start_date = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'start_date',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#start_date'
        }))

    end_date = forms.DateField(input_formats=['%Y-%m-%d'], widget=forms.TextInput(
        attrs={
            'class': 'form-control datetimepicker-input',
            'id': 'end_date',
            'value': datetime.now().strftime('%Y-%m-%d'),
            'data-toggle': 'datetimepicker',
            'data-target': '#end_date'
        }))

    search = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Ingrese una descripción para buscar',
        'autocomplete': 'off'
    }))

    mascots = forms.ModelChoiceField(queryset=Mascots.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    type_sale = forms.ChoiceField(choices=type_sale, widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    product_type = forms.ModelChoiceField(queryset=ProductType.objects.all(), widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    breedpet = forms.ChoiceField(choices=(), widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))

    type_medicalhistory = forms.ChoiceField(choices=type_medicalhistory, widget=forms.Select(
        attrs={
            'class': 'form-control select2',
            'style': 'width: 100%'
        }))
