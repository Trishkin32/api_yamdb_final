# Generated by Django 3.2.20 on 2023-10-02 09:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20230930_2153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='titlegenre',
            options={'verbose_name': 'Связь произведение-жанр', 'verbose_name_plural': 'Связь произведения-жанры'},
        ),
    ]
