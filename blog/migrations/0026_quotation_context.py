# Generated by Django 5.1.1 on 2024-10-11 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0025_entry_live_timezone"),
    ]

    operations = [
        migrations.AddField(
            model_name="quotation",
            name="context",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]