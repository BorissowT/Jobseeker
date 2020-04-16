from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .models import Company, Speciality, Vacancy



class MainView(View):
    def get(self, request):
        return render(request, "jobs/main.html", context={"specialities": Speciality.objects.all(),
                                                          "companies": Company.objects.all()})


class VacanciesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "jobs/vacancies.html", context={"vacancies": Vacancy.objects.all()})
        else:
            return redirect('/')


class JobsView(View):
    def get(self, request, id):
        return render(request, "jobs/jobs.html", context={"job": Vacancy.objects.filter(id=id).first()})


class CategoryView(View):
    def get(self, request, category):
        return render(request, "jobs/category.html")


class SendView(View):
    def get(self, request, id):
        return render(request, "jobs/send.html")


class CompaniesView(View):
    def get(self, request):
        return render(request, "jobs/companies.html")


class CompanyView(View):
    def get(self, request, id):
        return render(request, "jobs/company.html", context={"company": Company.objects.filter(id=id).first()})


class MyLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True

    # def get(self, request):
    #     if request.user.is_authenticated:
    #         return redirect('/')
    #     form = LoginForm()
    #     return render(request, self.template_name, {'form': form})
    #
    # def post(self, request):
    #     form = LoginForm(request.POST)
    #     if form.is_valid():
    #         username = form.username_check()
    #         password = form.password_check()
    #         user = authenticate(request, username=username, password=password)
    #         if user is not None:
    #             login(request, user)
    #             return redirect('/')
    #
    #     return render(request, self.template_name, {'form': form})


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'authentication/signup.html'



class ResumeView(View):
    def get(self, request):
        return render(request, "jobs/resume-create.html", context={})

class ResumeCreateView(View):
    def get(self, request):
        return render(request, "jobs/resume-edit.html", context={})
