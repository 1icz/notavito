from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def account(request):
    return render(request, 'users/account.html', {'user': request.user})