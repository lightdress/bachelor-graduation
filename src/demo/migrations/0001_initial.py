# Generated by Django 3.1.7 on 2021-06-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaperConfig',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=1024)),
                ('type', models.CharField(max_length=1024)),
                ('config', models.TextField(max_length=21844)),
            ],
        ),
    ]
