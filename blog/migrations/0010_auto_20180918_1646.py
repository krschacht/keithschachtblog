# Generated by Django 2.0b1 on 2018-09-18 16:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_import_ref'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='entry',
            options={'ordering': ('-created',), 'verbose_name_plural': 'Entries'},
        ),
        migrations.AlterField(
            model_name='blogmark',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
        migrations.AlterField(
            model_name='blogmark',
            name='metadata',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='comment',
            name='spam_status',
            field=models.CharField(choices=[('normal', 'Not suspected'), ('approved', 'Approved'), ('suspected', 'Suspected'), ('spam', 'SPAM')], max_length=16),
        ),
        migrations.AlterField(
            model_name='entry',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
        migrations.AlterField(
            model_name='entry',
            name='metadata',
            field=models.JSONField(blank=True, default=dict),
        ),
        migrations.AlterField(
            model_name='entry',
            name='tweet_html',
            field=models.TextField(blank=True, help_text='Paste in the embed tweet HTML, minus the script tag,\n        to display a tweet in the sidebar next to this entry.', null=True),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.utcnow),
        ),
        migrations.AlterField(
            model_name='quotation',
            name='metadata',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
