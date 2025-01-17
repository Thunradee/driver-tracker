# Generated by Django 3.2.6 on 2021-11-29 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('DRIVE_CLOCK', 'drive clock'), ('WORK_CLOCK', 'work clock')], max_length=11)),
                ('violationStatus', models.CharField(choices=[('V', 'violation'), ('OK', 'not in violation')], max_length=2)),
                ('timeValue', models.DurationField(help_text='HH:MM:SS')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('workStatus', models.CharField(choices=[('D', 'driving'), ('W', 'working'), ('OFF', 'off_duty')], max_length=3)),
                ('duration', models.DurationField(help_text='HH:MM:SS')),
            ],
        ),
    ]
