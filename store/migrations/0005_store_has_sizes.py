# Generated by Django 3.2 on 2022-06-12 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_alter_category_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='has_sizes',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
