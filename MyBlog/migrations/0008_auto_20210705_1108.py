# Generated by Django 3.1.7 on 2021-07-05 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyBlog', '0007_auto_20210705_1106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='author',
            field=models.CharField(max_length=14),
        ),
    ]
