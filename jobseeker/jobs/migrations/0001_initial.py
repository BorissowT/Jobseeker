# Generated by Django 3.0.5 on 2020-04-16 19:18

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
            name='Company',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('logo', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('employee_count', models.IntegerField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('picture', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=50)),
                ('skills', models.TextField()),
                ('salary_min', models.IntegerField()),
                ('salary_max', models.IntegerField()),
                ('published_at', models.DateField()),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='jobs.Company')),
                ('specialty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='jobs.Speciality')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=50)),
                ('salary', models.IntegerField()),
                ('specialty', models.CharField(max_length=50)),
                ('grade', models.CharField(max_length=50)),
                ('education', models.CharField(max_length=250)),
                ('experience', models.CharField(max_length=250)),
                ('portfolio', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('written_phone', models.CharField(max_length=50)),
                ('written_cover_letter', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
                ('vacancy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobs.Vacancy')),
            ],
        ),
    ]
