# Generated by Django 2.2.6 on 2022-08-01 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(max_length=300, verbose_name='текст поста'),
        ),
    ]
