# Generated by Django 5.1.1 on 2024-09-15 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_skilllevel_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='text',
            field=models.CharField(),
        ),
    ]
