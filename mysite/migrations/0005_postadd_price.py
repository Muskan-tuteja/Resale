# Generated by Django 2.1.7 on 2019-05-23 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0004_auto_20190523_1251'),
    ]

    operations = [
        migrations.AddField(
            model_name='postadd',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20, null=True),
        ),
    ]
