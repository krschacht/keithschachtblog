# Generated by Django 3.2.3 on 2021-08-07 22:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0016_series"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="series",
            options={"verbose_name_plural": "Series"},
        ),
    ]
