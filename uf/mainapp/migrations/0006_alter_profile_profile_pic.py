# Generated by Django 4.0.3 on 2022-04-19 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0005_alter_post_filecon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='static/default/default.png', upload_to='profile_pics/'),
        ),
    ]