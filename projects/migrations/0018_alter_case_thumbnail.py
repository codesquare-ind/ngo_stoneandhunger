# Generated by Django 3.2 on 2021-05-31 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_case_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='thumbnail',
            field=models.ImageField(blank=True, default='static/assets/img/default-thumbnail.jpg', null=True, upload_to=''),
        ),
    ]
