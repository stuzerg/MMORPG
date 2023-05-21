from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
import datetime


class newslist(models.Model):
    # Модель для списка подписчиков. Просто хранит только всех тех,
    # Кто согласен на рассылку.
    # Если честно, то из ТЗ
    # не очень понятно, кто и как хочет подписываться
    # и на какие новости
    subscriber = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)


class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    header = models.CharField(max_length=255)
    body = RichTextField(default='')
    staff_list = (('tanks', 'танки'), ('healers', 'лекари'), ('damagedealers', 'ДД'),
                  ('traders', 'торговцы'), ('gildmasters', 'гилды'),
                  ('questgivers', 'квестгиверы'), ('smiths', 'кузнецы'), ('skinners', 'кожевенники'),
                  ('potioners', 'зельевары'), ('spellcasters', 'заклинатели'))

    # поле staff(категории) тоже не понятно для чего будет еще использоваться
    # я не стал выводить её в отдельную модель

    staff = models.CharField(max_length=30, choices=staff_list, default='tanks', blank=False, verbose_name="профессия")

    def __str__(self):
        return self.header


class review(models.Model):
    # модель для откликов
    reviewpost = models.ForeignKey(post, on_delete=models.CASCADE, blank=False, verbose_name="отклик на пост")
    reviewuser = models.ForeignKey(User, verbose_name="отклик пользователя", on_delete=models.CASCADE, blank=False)
    reviewbody = models.CharField(max_length=255, default='void of emptiness', verbose_name="содержание поста")
    date_creation = models.DateTimeField(auto_now_add=True)
    acceptance = models.BooleanField(default=False, verbose_name="принято")   # поле для флага "принято" или "нет"
                                                                              # если отклик принят,
                                                                              # его всё равно можно будет удалить

    def __str__(self):
        return self.reviewbody
