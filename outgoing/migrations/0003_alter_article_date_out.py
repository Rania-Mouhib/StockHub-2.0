# Generated by Django 4.2.14 on 2024-08-13 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outgoing', '0002_alter_article_vnc'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='date_out',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
