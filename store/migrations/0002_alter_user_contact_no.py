# Generated by Django 3.2.9 on 2021-12-03 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='contact_no',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
    ]