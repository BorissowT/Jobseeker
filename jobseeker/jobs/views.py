from django.shortcuts import redirect, render
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

from .models import Company, Speciality, Vacancy, Resume, Application
from .forms import ApplicationForm, VacancyForm, CompanyForm, ResumeForm


class MainView(View):
    def get(self, request):
        return render(request, "jobs/main.html", context={"specialities": Speciality.objects.all(),
                                                          "companies": Company.objects.all(),
                                                          "main": True,})


class VacanciesView(View):
    def get(self, request):
        return render(request, "jobs/vacancies.html", context={"vacancies": Vacancy.objects.all()})


class VacancyView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            initial_data = {'name': "{} {}".format(request.user.first_name, request.user.last_name)}
        else:
            initial_data = {'name': " "}
        form = ApplicationForm(request.POST or None, initial=initial_data)
        return render(request, "jobs/vacancy.html", context={"vacancy": Vacancy.objects.filter(id=id).first(),
                                                             'form': form})

    def post(self, request, id):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            phone = form.clean_phone()
            name = form.clean_name()
            message = form.cleaned_message()
            Application.objects.create(written_username=name, written_phone=phone, written_cover_letter=message, vacancy=Vacancy.objects.filter(id=id).first(), user=request.user)
            if not form.errors:
                return render(request, "jobs/send.html")
        return render(request, "jobs/vacancy.html", context={"vacancy": Vacancy.objects.filter(id=id).first(),
                                                             'form': form})


class VacancyEditView(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            try:
                company = request.user.company
                if Vacancy.objects.filter(company=company, id=id).first():
                    is_updated=False
                    initial_data = {'title': Vacancy.objects.filter(id=id).first().title,
                                    'speciality': Vacancy.objects.filter(id=id).first().specialty.code,
                                    'salary_min': Vacancy.objects.filter(id=id).first().salary_min,
                                    'salary_max': Vacancy.objects.filter(id=id).first().salary_max,
                                    'skills': Vacancy.objects.filter(id=id).first().skills,
                                    'description': Vacancy.objects.filter(id=id).first().description}
                    form = VacancyForm(request.POST or None, initial=initial_data)
                    # delete = request.GET.get('delete')
                    return render(request, "jobs/vacancy-edit.html", context={"vacancy": Vacancy.objects.filter(company=company, id=id).first(),
                                                                              'form': form, 'is_updated': is_updated})
                else:
                    return redirect('/')
            except:
                return redirect('/')
        else:
            return redirect('/')

    def post(self, request, id):
        if request.user.is_authenticated:
            company_us = request.user.company
            form = VacancyForm(request.POST)
            vacancy = Vacancy.objects.filter(company=company_us, id=id).first()
            if form.is_valid():
                title = form.clean_title()
                speciality = form.clean_speciality()
                skills = form.clean_skills()
                salary_min = form.clean_salary_min()
                salary_max = form.clean_salary_max()
                description = form.clean_description()

                vacancy.title = title
                vacancy.speciality = Speciality.objects.filter(code=speciality).first()
                vacancy.skills = skills
                vacancy.salary_min = salary_min
                vacancy.salary_max = salary_max
                vacancy.description = description
                vacancy.save()
                is_updated = True
            else:
                is_updated = False
            return render(request, "jobs/vacancy-edit.html",
                          context={"vacancy": vacancy,
                                   'form': form, 'is_updated': is_updated})
        else:
            return redirect('/')


class VacancyCreateView(View):
    def get(self, request):
        if request.user.is_authenticated:
            form = VacancyForm(request.POST)
            is_updated = False
            return render(request, "jobs/vacancy-create.html", context={'form': form,'is_updated': is_updated})
        else:
            return redirect('/')

    def post(self, request):
        form = VacancyForm(request.POST)
        company = request.user.company
        if request.user.is_authenticated:
            if form.is_valid():
                title = form.clean_title()
                speciality = form.clean_speciality()
                skills = form.clean_skills()
                salary_min = form.clean_salary_min()
                salary_max = form.clean_salary_max()
                description = form.clean_description()
                speciality = Speciality.objects.filter(code=speciality).first()
                Vacancy.objects.create(title=title, specialty=speciality,
                                       skills=skills, salary_min=salary_min, salary_max=salary_max,
                                       description=description, company=company)
                is_updated = True
                return render(request, "jobs/vacancy-create.html", context={'form': form, 'is_updated': is_updated})
            else:
                is_updated = False
                return render(request, "jobs/vacancy-create.html", context={'form': form, 'is_updated': is_updated})
        else:
            return redirect('/')


class CategoryView(View):
    def get(self, request, category):
        return render(request, "jobs/category.html", context={"category": Speciality.objects.filter(code=category).first()})


class CompaniesView(View):
    def get(self, request):
        return render(request, "jobs/companies.html", context={"companies": Company.objects.all()})


class CompanyView(View):
    def get(self, request, id):
        return render(request, "jobs/company.html", context={"company": Company.objects.filter(id=id).first()})


class MyCompanyView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "jobs/company-create.html", context={"company": Company.objects.filter(user=request.user).first()})
        else:
            return redirect('/')


class MyCompanyEditView(View):
    def get(self, request):
        try:
            company = request.user.company
        except:
            company = None
        if request.user.is_authenticated:
            if company == None:
                form = CompanyForm(request.POST or None)
                return render(request, "jobs/company-edit.html", context={"form":form})
            else:
                initial_data = {"name":company.name, "location":company.location, "description": company.description,
                                "employee_count": company.employee_count, 'logo': company.logo}
                form = CompanyForm(request.POST or None, initial=initial_data)
                return render(request, "jobs/company-edit.html", context={"form": form})
        else:
            return redirect('/')

    def post(self, request):
        if request.user.is_authenticated:
            try:
                company = request.user.company
            except:
                company = None
            form = CompanyForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                data = form.cleaned_data
                if company == None:
                    Company.objects.create(name=data["name"], location=data['location'], logo=data['logo'],
                                           employee_count=data['employee_count'], description=data['description'],
                                           user=request.user)
                    is_created = True
                    return render(request, "jobs/company-edit.html", context={"form": form, 'is_created':is_created})
                else:
                    if data['logo']!=None:
                        company.logo = data['logo']
                    company.name = data["name"]
                    company.location = data['location']
                    company.employee_count = data['employee_count']
                    company.description = data['description']
                    company.user = request.user
                    company.save()
                    is_updated = True
                    return render(request, "jobs/company-edit.html", context={"form": form, 'is_updated': is_updated})
        else:
            return redirect('/')


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
            try:
                resume = request.user.resume
            except:
                resume = None
            if resume != None:
                initial_data = {"name": request.user.first_name, "surname": request.user.last_name,
                                'status': resume.status, 'salary': resume.salary, 'speciality': resume.specialty,
                                'grade': resume.grade, 'education': resume.education, 'experience': resume.experience,
                                'portfolio': resume.portfolio}
                form = ResumeForm(request.POST or None, initial=initial_data)
                return render(request, "jobs/resume-edit.html", context={"resume": resume, 'form': form})
            else:
                initial_data = {"name": request.user.first_name, "surname": request.user.last_name}
                form = ResumeForm(request.POST or None, initial=initial_data)
                return render(request, "jobs/resume-edit.html", context={'form': form})
        else:
            return redirect('/')

    def post(self, request):
        try:
            resume = request.user.resume
        except:
            resume = None
        if request.user.is_authenticated:
            form = ResumeForm(request.POST or None)
            if form.is_valid():
                data = form.cleaned_data
                if resume == None:
                    Resume.objects.create(status=data["status"], portfolio=data["portfolio"], specialty=data["speciality"],
                                          grade=data["grade"], education=data["education"], salary=data["salary"],
                                          experience=data["experience"], user=request.user)
                    user = User.objects.filter(username=request.user.username).first()
                    user.first_name = data["name"]
                    user.last_name = data["surname"]
                    user.save()
                    is_created = True
                    return render(request, "jobs/resume-edit.html", context={'form': form, 'is_created': is_created})
                else:
                    resume.status = data["status"]
                    resume.portfolio = data["portfolio"]
                    resume.specialty = data["speciality"]
                    resume.grade = data["grade"]
                    resume.education = data["education"]
                    resume.salary = data["salary"]
                    resume.experience = data["experience"]
                    resume.save()

                    user = User.objects.filter(username=request.user.username).first()
                    user.first_name = data["name"]
                    user.last_name = data["surname"]
                    user.save()
                    is_updated = True
                    return render(request, "jobs/resume-edit.html", context={'form': form, 'is_updated': is_updated})
            else:
                return render(request, "jobs/resume-edit.html", context={'form': form})
        else:
            return redirect('/')
