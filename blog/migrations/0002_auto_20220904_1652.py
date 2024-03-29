# Generated by Django 3.0.3 on 2022-09-04 15:52

import ckeditor.fields
import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=ckeditor.fields.RichTextField(help_text='Edit and enter text just like MS Word.', verbose_name='Blog'),
        ),
        migrations.AlterField(
            model_name='post',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 4, 15, 52, 47, 691571, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_picture',
            field=models.ImageField(null=True, upload_to='post_pic/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='post',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 4, 15, 52, 47, 691571, tzinfo=utc)),
        ),
    ]
