# Generated by Django 2.2.4 on 2019-08-21 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorials', '0004_comment_upvote'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='pub_date',
            field=models.DateTimeField(default=None, verbose_name='date published'),
            preserve_default=False,
        ),
    ]
