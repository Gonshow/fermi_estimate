# Generated by Django 3.1.2 on 2021-01-17 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_comment_depth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='depth',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='深さ'),
        ),
    ]
