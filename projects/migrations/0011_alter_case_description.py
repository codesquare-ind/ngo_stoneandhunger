# Generated by Django 3.2 on 2021-05-08 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_alter_case_date_of_initiation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='description',
            field=models.CharField(blank=True, max_length=1055, null=True),
        ),
    ]
