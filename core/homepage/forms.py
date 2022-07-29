from django.forms import ModelForm
from django import forms

from core.homepage.models import *


class MainpageForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True
        for input in self.visible_fields():
            input.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off'
            })

    class Meta:
        model = Mainpage
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'ruc': forms.TextInput(attrs={'placeholder': 'Ingrese un ruc'}),
            'iva': forms.TextInput(),
            'proprietor': forms.TextInput(attrs={'placeholder': 'Ingrese un propietario'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'with_us': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'mission': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'vision': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'about_us': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
            'phone': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono fijo'}),
            'mobile': forms.TextInput(attrs={'placeholder': 'Ingrese un teléfono celular'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ingrese un email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección'}),
            'coordinates': forms.TextInput(attrs={'placeholder': 'Ingrese sus coordendas'}),
            'horary': forms.TextInput(attrs={'placeholder': 'Ingrese su horario'}),
            'experiencia': forms.TextInput(attrs={'placeholder': 'Ingrese los años de experiencia'}),
            'about_youtube': forms.TextInput(attrs={'placeholder': 'Ingrese un enlace de youtube'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SocialNetworksForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['css'].widget.attrs['autofocus'] = True

    class Meta:
        model = SocialNetworks
        fields = '__all__'
        widgets = {
            'css': forms.TextInput(attrs={'placeholder': 'Ingrese una clase css'}),
            'icon': forms.TextInput(attrs={'placeholder': 'Ingrese un icono font-awesome'}),
            'url': forms.TextInput(attrs={'placeholder': 'Ingrese una dirección web'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ServicesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Services
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class DepartmentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Departments
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'title': forms.TextInput(attrs={'placeholder': 'Ingrese un titulo'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class StatisticsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Statistics
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'cant': forms.TextInput(),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class FreqQuestionsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget.attrs['autofocus'] = True

    class Meta:
        model = FreqQuestions
        fields = '__all__'
        widgets = {
            'question': forms.Textarea(attrs={'placeholder': 'Ingrese una pregunta', 'rows': 4, 'cols': 4}),
            'answer': forms.Textarea(attrs={'placeholder': 'Ingrese una respuesta', 'rows': 4, 'cols': 4}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TestimonialsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Testimonials
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'job': forms.TextInput(attrs={'placeholder': 'Ingrese un cargo'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese un comentario', 'rows': 3, 'cols': 3}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class GalleryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Gallery
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TeamForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Team
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={
                'placeholder': 'Ingrese un nombre',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'job': forms.TextInput(attrs={
                'placeholder': 'Ingrese un cargo',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'phrase': forms.TextInput(attrs={
                'placeholder': 'Ingrese una frase',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'desc': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                'class': 'form-control',
                'autocomplete': 'off',
                'rows': 3,
                'cols': 3,
            }),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class CommentsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['names'].widget.attrs['autofocus'] = True

    class Meta:
        model = Comments
        fields = '__all__'
        widgets = {
            'names': forms.TextInput(attrs={
                'placeholder': 'Ingrese un nombre',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'email': forms.TextInput(attrs={
                'placeholder': 'Ingrese un email',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'mobile': forms.TextInput(attrs={
                'placeholder': 'Ingrese un número de teléfono',
                'class': 'form-control',
                'autocomplete': 'off'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Ingrese una descripción',
                'class': 'form-control',
                'autocomplete': 'off',
                'rows': 4,
                'cols': 4,
            }),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class QualitiesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Qualities
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ingrese un nombre'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'rows': 3, 'cols': 3}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class NewsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.attrs['autofocus'] = True

    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ingrese un título'}),
            'desc': forms.Textarea(attrs={'placeholder': 'Ingrese una descripción', 'cols': 5, 'rows': 5}),
            'url': forms.TextInput(attrs={'placeholder': 'Ingrese un enlace web'}),
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data


class VideosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['autofocus'] = True

    class Meta:
        model = Videos
        fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Ingrese un título'}),
            'url': forms.TextInput(attrs={'placeholder': 'Ingrese una url'}),
        }
        exclude = ['date_joined']

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except:
            pass
        return data
