# Generated by Django 3.2.3 on 2021-05-30 17:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whizapp', '0006_commentreply_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentreply',
            name='user',
        ),
    ]
