# Generated by Django 3.2.20 on 2023-09-30 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_confirmation_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='confirmation_code',
            field=models.CharField(default='Yv1U6rOnnVbF23v', editable=False, max_length=10),
        ),
    ]