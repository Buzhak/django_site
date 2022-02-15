from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from accounts.forms import UserLoginForm, Ures_Registration_form, User_update_form

User = get_user_model()


def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')
        user = authenticate(request, email=email, password=password)
        login(request, user)
        messages.success(request, 'Вы вошли на сайт')
        return redirect('home')
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('home')

def register_view(request):
    form = Ures_Registration_form(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        messages.success(request, 'Пользователь зарегистрирован!')
        return render(request, 'accounts/register_done.html', {'new_user': new_user})
    return render(request, 'accounts/register.html', {'form': form})

def update_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = User_update_form(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                user.city = data['city']
                user.language = data['language']
                user.send_email = data['send_email']
                user.save()
                messages.success(request, 'Настройки рассылки обновлены')
                return redirect('accounts:update')
        
        form = User_update_form(initial={'city': user.city, 'language': user.language, 'send_email': user.send_email})
        return render(request, 'accounts/update.html', {'form': form})
    else:
        return redirect('accounts:login')

def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
            messages.error(request, 'Пользователь удалён!')
    return redirect('home')