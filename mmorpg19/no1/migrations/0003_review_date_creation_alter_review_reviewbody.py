# Generated by Django 4.1.5 on 2023-05-16 15:12

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('no1', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date_creation',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='review',
            name='reviewbody',
            field=models.CharField(default='void of emptiness', max_length=255),
        ),
    ]
