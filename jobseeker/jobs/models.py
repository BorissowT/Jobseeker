from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

import datetime

from phone_field import PhoneField


class Company(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=settings.MEDIA_COMPANY_IMAGE_DIR, default='/media/specty_management.png')
    description = models.TextField()
    employee_count = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')

    def __str__(self):
        return "{} ({})".format(self.name, self.id)


class Speciality(models.Model):
    id = models.IntegerField(primary_key=True)
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to=settings.MEDIA_SPECIALITY_IMAGE_DIR)

    def __str__(self):
        return "{} ({})".format(self.code, self.id)


class Vacancy(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=50)
    specialty = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.TextField()
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    description = models.TextField()
    published_at = models.DateField(default=datetime.date.today)

    def __str__(self):
        return "{} ({})".format(self.title, self.company.name)


class Resume(models.Model):
    id = models.IntegerField(primary_key=True)
    status = models.CharField(max_length=50)
    salary = models.IntegerField()
    specialty = models.CharField(max_length=50)
    grade = models.CharField(max_length=50)
    education = models.CharField(max_length=250)
    experience = models.CharField(max_length=250)
    portfolio = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='resume')


class Application(models.Model):
    id = models.IntegerField(primary_key=True)
    written_username = models.CharField(max_length=50)
    written_phone = PhoneField(max_length=50)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')



