# Generated by Django 4.2.7 on 2023-11-17 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_schedule_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='status',
            field=models.CharField(choices=[('1', 'Active'), ('0', 'Cancelled')], default=1, max_length=2),
        ),
    ]
