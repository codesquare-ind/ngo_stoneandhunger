# Generated by Django 3.2 on 2021-06-02 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0018_alter_case_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='total_online',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]
