# Generated by Django 4.0.3 on 2022-04-14 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='filecon',
            field=models.FileField(null=True, upload_to='user_post_files'),
        ),
    ]
