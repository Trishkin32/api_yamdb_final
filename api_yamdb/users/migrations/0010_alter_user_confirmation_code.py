# Generated by Django 3.2.20 on 2023-10-01 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20230930_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='qpAUmQQVvdDStnG', editable=False, max_length=150),
        ),
    ]