# Generated by Django 4.2.3 on 2023-09-16 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0001_initial'),
        ('leads', '0003_lead_team'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='team.team'),
        ),
    ]
