# Generated by Django 4.2.6 on 2023-11-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_host', models.TextField(blank=True, null=True)),
                ('email_port', models.TextField(blank=True, null=True)),
                ('email_use_tls', models.BooleanField(default=True)),
                ('email_from_email', models.TextField(blank=True, null=True)),
                ('email_host_user', models.TextField(blank=True, null=True)),
                ('email_host_password', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
