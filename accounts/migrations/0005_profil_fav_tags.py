# Generated by Django 3.0.4 on 2020-03-29 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200329_1427'),
        ('accounts', '0004_auto_20200329_2036'),
    ]

    operations = [
        migrations.AddField(
            model_name='profil',
            name='fav_tags',
            field=models.ManyToManyField(to='blog.Tag'),
        ),
    ]
