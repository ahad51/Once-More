# Generated by Django 5.1.4 on 2025-01-15 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topicTasks', '0008_remove_task_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='Untitled', max_length=255),
        ),
    ]
