from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView

from .models import Company, Speciality, Vacancy, Resume


class MainView(View):
    def get(self, request):
        return render(request, "jobs/main.html", context={"specialities": Speciality.objects.all(),
                                                          "companies": Company.objects.all()})


class VacanciesView(View):
    def get(self, request):
            return render(request, "jobs/vacancies.html", context={"vacancies": Vacancy.objects.all()})



class VacancyView(View):
    def get(self, request, id):
        return render(request, "jobs/vacancy.html", context={"vacancy": Vacancy.objects.filter(id=id).first()})


class VacancyEditView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                company = request.user.company
                if Vacancy.objects.filter(company=company, id=id).first():
                    return render(request, "jobs/vacancy-edit.html", context={"vacancy": Vacancy.objects.filter(company=company, id=id).first()})
                else:
                    return redirect('/')
            except:
                return redirect('/')
        else:
            return redirect('/')


class CategoryView(View):
    def get(self, request, category):
        print(Speciality.objects.filter(code=category).first().title)
        return render(request, "jobs/category.html", context={"category": Speciality.objects.filter(code=category).first()})


class SendView(View):
    def get(self, request, id):
        return render(request, "jobs/send.html")


class CompaniesView(View):
    def get(self, request):
        return render(request, "jobs/companies.html", context={"companies": Company.objects.all()})


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
        if request.user.is_authenticated and Resume.objects.filter(user=request.user).first()==None:
            return render(request, "jobs/resume-create.html", context={})
        elif request.user.is_authenticated and Resume.objects.filter(user=request.user).first():
            return redirect('/myresume/edit')
        else:
            return redirect('/')


class ResumeCreateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            resume = Resume.objects.filter(user=request.user).first()
            return render(request, "jobs/resume-edit.html", context={"resume": resume})
        else:
            return redirect('/')


class MyCompanyView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "jobs/company-create.html", context={"company": Company.objects.filter(user=request.user).first()})
        else:
            return redirect('/')


class MyCompanyEditView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "jobs/company-edit.html", context={})
        else:
            return redirect('/')