from datetime import datetime, timedelta
import email
from random import randint

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.urls import reverse


from .models import verificationtable


# Create your views here.
def register(request):
    data = {'code':''}
    if request.method == 'POST' and request.POST.get('button') == "зарегистрироваться и отправить на почту код" :

        emails = list(User.objects.values_list(('email'), flat=True))   # создание списка уже зарегистрированных имен и емэйлов
        names = list(User.objects.values_list(('username'), flat=True))

        one_minute_ago = datetime.now() - timedelta(minutes=1)    # метка времени минуту назад
        old_records_in_vtable = verificationtable.objects.filter(vtime__lt=one_minute_ago)

        old_records_in_vtable.delete()  # удаляем записи с временем жизни более одной минуты

        emails.extend(list(verificationtable.objects.values_list(('mailbox'), flat=True)))  #   добавляем в emails и names
        names.extend(list(verificationtable.objects.values_list(('vname'), flat=True)))     #   пользователей, которые пытаются
                                                                                            #   зарегистрироваться в текущей минуте
                                                                                            #  чтоб исключить дублирование имен
                                                                                            #  при одновременной регистрации
                                                                                            #  разных пользователей

        reg_email = request.POST.get('email')
        reg_name = request.POST.get('username')

        print(request.POST.get('username'))
        print(request.POST.get('password'))
        print(request.POST.get('email'))
        if reg_email in emails:
            response = HttpResponse("email уже зарегистрирован")
            return response
        if reg_name in names:
            response = HttpResponse("имя уже зарегистрировано")
            return response


        cod = str(randint(10000, 99999))[1:]   # четырёхзначный код верификации, 0000-9999
        print(cod)
        if verificationtable.objects.filter(mailbox=email).exists:
            verificationtable.objects.filter(mailbox=email).delete()

        rec = verificationtable(mailbox=reg_email, vcode=cod, vtime=datetime.now(),   # запись креденшилов
                                                                                      # во временную таблицу
                                vname=reg_name, vpass=request.POST.get('password'))
        rec.save()

        print("отправка кода на", reg_email)
        send_mail(
            subject='Ваш одноразовый код для подтверждения регистрации',
            message=f'Ваш код {cod} действителен в течении 60 секунд',
            from_email='stutzerg@yandex.ru',
            recipient_list=['stutzerg@list.ru', reg_email] # добавил себя для контроля
        )

        return HttpResponseRedirect(reverse("verifysecondstage")+f"?reg_email={reg_email}")

    return render(request,'sign.html',data)

def verificate_me(request):
    email=(request.GET['reg_email'])
    print('email',email)
    cod = verificationtable.objects.get(mailbox=email).vcode

    print('время записи ',verificationtable.objects.get(mailbox=email).vtime)
    print('время django ', datetime.now())


    if request.method == 'POST': # создание нового пользователя
        correct_code = str(cod) == request.POST.get('code')
        temp_user_credentials = verificationtable.objects.get(mailbox=email)
        lifetime60sec = (datetime.now() - (temp_user_credentials.vtime).replace(tzinfo=None)).seconds < 60

        if all([correct_code, lifetime60sec]):   # проверка кода и его времени жизни
            new_user = User.objects.create_user(username=(temp_user_credentials.vname),
                            email=email,
                            password=(temp_user_credentials.vpass))
            new_user.save()
            login(request, user=new_user)
            temp_user_credentials.delete()
            return render(request,'succesreg.html')

        else:
            return HttpResponse('код верификации устарел или неверный')

    return render(request, 'secondstageverify.html', {'kode': cod})   # в форму вывожу подсказку с кодом, чтоб не лезть в почту



