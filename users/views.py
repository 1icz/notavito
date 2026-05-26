from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .forms import CustomUserCreationForm, UserUpdateForm, CustomPasswordChangeForm


def signup(request):
    """Регистрация нового пользователя"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def account(request):
    """Личный кабинет пользователя"""
    return render(request, 'users/account.html', {'user': request.user})


@login_required
def edit_profile(request):
    """Редактирование профиля (имя, email, пароль)"""
    if request.method == 'POST':
        # Обработка изменения пароля
        if 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Чтобы не разлогинило
                messages.success(request, 'Пароль успешно изменён!')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Ошибка при смене пароля. Проверьте правильность ввода.')
        else:
            # Обработка изменения профиля
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Профиль успешно обновлён!')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Ошибка при обновлении профиля.')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'users/edit_profile.html', {
        'user_form': user_form,
        'password_form': password_form,
    })