# Generated by Django 2.2.5 on 2020-05-20 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_comment_comment_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='id',
            field=models.AutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_id',
            field=models.CharField(max_length=1000),
        ),
    ]
