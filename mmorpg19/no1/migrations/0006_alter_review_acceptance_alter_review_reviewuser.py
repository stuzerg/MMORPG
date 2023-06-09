# Generated by Django 4.1.5 on 2023-05-17 08:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('no1', '0005_review_reviewuser'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='acceptance',
            field=models.BooleanField(default=False, verbose_name='принято'),
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewuser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='отклик пользователя'),
        ),
    ]
