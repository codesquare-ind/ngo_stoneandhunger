# Generated by Django 3.2 on 2021-06-03 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0019_case_total_online'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='priority',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
