from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import BaseRegisterForm
from .forms import UserTryingLog


class my_login1(LoginView):
    model = User
    form_class = BaseRegisterForm
    template_name = 'login.html'
    success_url = 'all/'
def my_login2(request):
    form = UserTryingLog()

    success_url = 'main/index.html'
    data = {}
    if request.method == 'POST':
        print(request.POST.get('username'))
        print(request.POST.get('password'))
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            print('login OK')
            print(user.get_user_permissions())
            return redirect('/all')
        else:

            print('login fault')

    return render(request, 'logtesting.html', data)
