# Generated by Django 2.0.3 on 2019-06-19 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('futground', '0002_auto_20190620_0119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='ending_time',
            field=models.TimeField(),
        ),
    ]
