# Generated by Django 2.1rc1 on 2018-09-09 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Blogger', '0002_post_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.BooleanField(default=False),
        ),
    ]
