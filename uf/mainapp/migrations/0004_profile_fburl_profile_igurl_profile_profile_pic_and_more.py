# Generated by Django 4.0.3 on 2022-04-15 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fburl',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='igurl',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='twitterurl',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='websiteurl',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
