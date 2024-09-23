# Generated by Django 4.2.14 on 2024-08-26 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('outgoing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_articles', to='inventory.model'),
        ),
        migrations.AlterField(
            model_name='article',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outgoing_articles', to='inventory.type'),
        ),
    ]
