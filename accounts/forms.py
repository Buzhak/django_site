from multiprocessing import AuthenticationError
from django import forms 
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clearn(self, *args, **kwargs):
        email = self.changed_data.get('email')
        password = self.changed_data.get('password')

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет.')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Неверный пароль.')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключёню.')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class Ures_Registration_form(forms.ModelForm):

    email = forms.CharField(label='Введите email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    
    class Meta():
        model = User
        fields = ('email', )

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают!')
        return data['password2']