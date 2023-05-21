from datetime import datetime

from django.core.mail import send_mail
from .models import newslist


def send_spam():

        Victim_list = list(newslist.objects.values_list(('subscriber__email'), flat=True))
        send_mail(
            subject='Вам новостная рассылка из MMORPGa',
            message='Тут будут новости',
            from_email='stutzerg@yandex.ru',
            recipient_list=Victim_list
        )
        print(f'текущее время: {datetime.now()} , Рассылка будет отправлена на {Victim_list}')
