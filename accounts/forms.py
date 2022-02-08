from multiprocessing import AuthenticationError
from socket import fromshare
from django import forms 
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.CharFild(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password = forms.CharField(wiget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clearn(self, *args, **kwargs):
        email = self.changed_data.get('email')
        password = self.changed_data.get('password')

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такеого пользователя нет.')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Неверный пароль.')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключён')
        return super(UserLoginForm, self).clean(*args, **kwargs)
