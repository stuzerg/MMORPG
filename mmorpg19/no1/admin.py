# Register your models here.
from django.contrib import admin

from .models import post, review


# class PostAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = ['body', 'type_post', "addit_prop"] # генерируем список имён всех полей для более красивого отображения
    # list_filter = ('cat', 'type_post')

admin.site.register(post)
admin.site.register(review)