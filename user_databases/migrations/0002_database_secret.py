# Generated by Django 2.2.7 on 2019-11-24 17:20

from django.db import migrations, models
import user_databases.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_databases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='secret',
            field=models.TextField(default=user_databases.models.generateSecret, unique=True),
        ),
    ]