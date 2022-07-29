from django import forms

from core.user.models import User


class ResetPasswordForm(forms.Form):
    dni = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Ingrese su número de cedula',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        users = User.objects.filter(dni=cleaned['dni'])
        if not users.exists():
            raise forms.ValidationError('El username no existe')
            #self._errors['error'] = self._errors.get('error', self.error_class())
            #self._errors['error'].append('El username no existe')
        return cleaned

    def get_user(self):
        dni = self.cleaned_data.get('dni')
        return User.objects.get(dni=dni)


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Ingrese un password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita el password',
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    def clean(self):
        cleaned = super().clean()
        password = cleaned['password']
        confirmPassword = cleaned['confirmPassword']
        if password != confirmPassword:
            raise forms.ValidationError('Las contraseñas deben ser iguales')
        return cleaned
