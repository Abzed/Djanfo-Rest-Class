# Generated by Django 4.0.3 on 2022-12-10 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='student',
        ),
        migrations.AddField(
            model_name='classroom',
            name='student',
            field=models.ManyToManyField(blank=True, to='api.student'),
        ),
    ]
