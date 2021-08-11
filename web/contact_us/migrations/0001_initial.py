# Generated by Django 3.1.7 on 2021-08-11 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('content', models.TextField()),
                ('file', models.FileField(blank=True, null=True, upload_to='feedback_files/')),
            ],
            options={
                'verbose_name': 'Feedback',
            },
        ),
    ]
