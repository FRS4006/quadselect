# Generated by Django 4.0 on 2024-03-12 20:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('logic', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='topics',
        ),
        migrations.AddField(
            model_name='participantsession',
            name='topic',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='logic.topic'),
            preserve_default=False,
        ),
    ]
