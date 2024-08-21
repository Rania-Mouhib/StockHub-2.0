# Generated by Django 4.2.14 on 2024-08-06 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('Type1', 'Type1'), ('Type2', 'Type2')], max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('vnc', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('bci', models.CharField(blank=True, max_length=100, null=True)),
                ('plant', models.CharField(choices=[('BSK1', 'BSK1'), ('BSK2', 'BSK2'), ('BSK3', 'BSK3'), ('BSK4', 'BSK4')], max_length=4)),
                ('date_in', models.DateField()),
                ('pilot', models.CharField(blank=True, max_length=100, null=True)),
                ('rack', models.CharField(choices=[('A1', 'A1'), ('A2', 'A2'), ('A3', 'A3'), ('A4', 'A4'), ('A5', 'A5'), ('A6', 'A6'), ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('B5', 'B5'), ('B6', 'B6'), ('C1', 'C1'), ('C2', 'C2'), ('C3', 'C3'), ('C4', 'C4'), ('C5', 'C5'), ('C6', 'C6'), ('D1', 'D1'), ('D2', 'D2'), ('D3', 'D3'), ('D4', 'D4'), ('D5', 'D5'), ('D6', 'D6'), ('E1', 'E1'), ('E2', 'E2'), ('E3', 'E3'), ('E4', 'E4'), ('E5', 'E5'), ('E6', 'E6'), ('F1', 'F1'), ('F2', 'F2'), ('F3', 'F3'), ('F4', 'F4'), ('F5', 'F5'), ('F6', 'F6'), ('G1', 'G1'), ('G2', 'G2'), ('G3', 'G3'), ('G4', 'G4'), ('G5', 'G5'), ('G6', 'G6'), ('H1', 'H1')], max_length=2)),
                ('comment', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
