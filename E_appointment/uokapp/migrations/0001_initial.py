# Generated by Django 2.2.5 on 2020-08-26 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion_date', models.DateField(blank=True, default=None)),
                ('suggestion_hour', models.TimeField(blank=True, default=None, null=True)),
                ('end_time', models.TimeField(blank=True, default=None, null=True)),
                ('student_reason', models.TextField(blank=True, max_length=1000)),
                ('status', models.CharField(blank=True, choices=[('accepted', 'accepted'), ('rejected', 'rejected'), ('canceled', 'canceled')], default=None, max_length=9, null=True)),
                ('suggested_date', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.PositiveIntegerField()),
                ('student', models.BooleanField(default=True)),
                ('interns', models.BooleanField(default=False)),
                ('depart', models.CharField(choices=[('BIT', 'Information Technology'), ('BBIT', 'Business & Information Technology'), ('BCS', 'Computer Sciences')], max_length=5)),
                ('session', models.CharField(choices=[('Day', 'day'), ('Evening', 'evening'), ('Weekend', 'weekend')], max_length=7)),
                ('campus', models.CharField(choices=[('Kigali', 'Kigali'), ('Musanze', 'Musanze'), ('Nyanza', 'Nyanza')], max_length=7)),
                ('profile', models.ImageField(blank=True, default='media/profile_pics/westbl_dFbRfcB.jpg', upload_to='profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='staffs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.PositiveIntegerField()),
                ('ViceChancellor', models.BooleanField(default=False)),
                ('DVCA', models.BooleanField(default=False)),
                ('dean', models.BooleanField(default=False)),
                ('HOD', models.BooleanField(default=False)),
                ('lecturer', models.BooleanField(default=False)),
                ('registror', models.BooleanField(default=False)),
                ('CFO', models.BooleanField(default=False)),
                ('faculty', models.CharField(blank=True, choices=[('IT & Architecture', 'IT & Architecture'), ('Law Administration', 'Law Administration'), ('Finance', 'Finance')], max_length=19)),
                ('campus', models.CharField(choices=[('Kigali', 'Kigali'), ('Musanze', 'Musanze'), ('Nyanza', 'Nyanza')], max_length=7)),
                ('profile', models.ImageField(blank=True, default=None, upload_to='profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='othersuggestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion_date', models.DateField(blank=True, default=None)),
                ('suggestion_hour', models.TimeField(blank=True, default=None, null=True)),
                ('end_time', models.TimeField(blank=True, default=None, null=True)),
                ('reason', models.TextField(max_length=1000)),
                ('status', models.CharField(blank=True, choices=[('accepted', 'accepted'), ('rejected', 'rejected'), ('canceled', 'canceled')], default=None, max_length=9, null=True)),
                ('requested_date', models.DateTimeField(auto_now_add=True)),
                ('seen', models.BooleanField(default=False)),
                ('appointment', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='othersuggestion', to='uokapp.appointment')),
                ('staffsuggestion', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='uokapp.staffs')),
                ('studentsuggestion', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='uokapp.student')),
            ],
        ),
        migrations.AddField(
            model_name='appointment',
            name='lecture',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='uokapp.staffs'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='student',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='uokapp.student'),
        ),
    ]