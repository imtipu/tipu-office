# Generated by Django 2.1.5 on 2019-03-04 16:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('myApp', '0002_attendence'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendence',
            name='attendence_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]