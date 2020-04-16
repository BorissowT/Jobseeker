"""jobseeker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from jobs.views import MainView, VacanciesView, JobsView, CategoryView, CompanyView, MyLoginView, MySignupView, ResumeView, ResumeCreateView


urlpatterns = [
    path('', MainView.as_view()),
    path('vacancies/', VacanciesView.as_view()),

    path('jobs/<int:id>/', JobsView.as_view()),
    # path('jobs/<int:id>/send/', SendView.as_view()),
    path('jobs/cat/<str:category>/', CategoryView.as_view()),

    # path('companies/', CompaniesView.as_view()),
    path('company/<int:id>/', CompanyView.as_view()),

    path('admin/', admin.site.urls)
]
urlpatterns += [
path('resume', ResumeView.as_view()),
path('resume/create', ResumeCreateView.as_view()),
]
urlpatterns += [
    path('login/', MyLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('signup', MySignupView.as_view()),
]