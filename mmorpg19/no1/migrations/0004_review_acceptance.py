# Generated by Django 4.1.5 on 2023-05-16 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('no1', '0003_review_date_creation_alter_review_reviewbody'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='acceptance',
            field=models.BooleanField(default=False),
        ),
    ]
