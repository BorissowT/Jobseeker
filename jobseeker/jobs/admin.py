from django.contrib import admin
from django.contrib.auth.models import User

from .models import Speciality, Company, Vacancy,  Resume, Application
# Register your models here.

# class UserAdmin(admin.ModelAdmin):
#     pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class SpecialityAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass


class ResumeAdmin(admin.ModelAdmin):
    pass


class ApplicationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Company, CompanyAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(Application, ApplicationAdmin)
# admin.site.register(User, UserAdmin)