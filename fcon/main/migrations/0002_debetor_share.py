# Generated by Django 4.0.5 on 2022-07-18 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='debetor',
            name='share',
            field=models.IntegerField(null=True),
        ),
    ]
