from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from .forms import ApplicationForm, VacancyForm, CompanyForm, ResumeForm, SearchForm, EditCompanyForm
from .models import Company, Speciality, Vacancy, Resume, Application


class MainView(View):
    def get(self, request):
        form = SearchForm()
        return render(request, "jobs/main.html", context={"specialities": Speciality.objects.all(),
                                                          "companies": Company.objects.all(),
                                                          "main": True,
                                                          "form": form})


class VacanciesView(View):
    def get(self, request):
        return render(request, "jobs/vacancies.html", context={"vacancies": Vacancy.objects.all()})


class VacancyView(View):
    def get(self, request, id):
        if Vacancy.objects.filter(id=id).first():
            if request.user.is_authenticated:
                initial_data = {'name': "{} {}".format(request.user.first_name, request.user.last_name)}
            else:
                initial_data = {'name': " "}
            form = ApplicationForm(request.POST or None, initial=initial_data)
            return render(request, "jobs/vacancy.html", context={"vacancy": Vacancy.objects.filter(id=id).first(),
                                                                 'form': form})
        else:
            raise Http404

    def post(self, request, id):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            date = form.cleaned_data
            date.update({'vacancy': Vacancy.objects.filter(id=id).first()})
            date.update({'user': request.user})
            Application.objects.create(**date)
            return render(request, "jobs/send.html")
        return render(request, "jobs/vacancy.html", context={"vacancy": Vacancy.objects.filter(id=id).first(),
                                                             'form': form})


class VacancyEditView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return redirect('/')
        if not hasattr(request.user, 'company'):
            return redirect('/')
        company = request.user.company
        if not Vacancy.objects.filter(company=company, id=id).first():
            return HttpResponse("Access Error")
        is_updated = False
        init = Vacancy.objects.filter(id=id).first()
        initial_data = {'title': init.title,
                        'specialty': init.specialty.code,
                        'salary_min': init.salary_min,
                        'salary_max': init.salary_max,
                        'skills': init.skills,
                        'description': init.description}
        form = VacancyForm(request.POST or None, initial=initial_data)
        return render(request, "jobs/vacancy-edit.html", context={"vacancy": Vacancy.objects.filter(company=company, id=id).first(),
                                                                  'form': form,
                                                                  'is_updated': is_updated})

    def post(self, request, id):
        if not request.user.is_authenticated:
            return redirect('/')
        form = VacancyForm(request.POST)
        vacancy = Vacancy.objects.filter(company=request.user.company, id=id).first()
        if form.is_valid():
            data = form.cleaned_data
            data['specialty'] = Speciality.objects.filter(code=data['specialty']).first()
            Vacancy.objects.filter(company=request.user.company, id=id).update(**data)
            is_updated = True
        else:
            is_updated = False
        return render(request, "jobs/vacancy-edit.html", context={"vacancy": vacancy, 'form': form, 'is_updated': is_updated})


class VacancyCreateView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        form = VacancyForm(request.POST)
        is_updated = False
        return render(request, "jobs/vacancy-create.html", context={'form': form,'is_updated': is_updated})

    def post(self, request):
        form = VacancyForm(request.POST)
        company = request.user.company
        if not request.user.is_authenticated:
            return redirect('/')
        if form.is_valid():
            data = form.cleaned_data
            title = data["title"]
            speciality = data["speciality"]
            skills = data["skills"]
            salary_min = form.clean_salary_min()
            salary_max = form.clean_salary_max()
            description = data["description"]
            speciality = Speciality.objects.filter(code=speciality).first()
            Vacancy.objects.create(title=title,
                                   specialty=speciality,
                                   skills=skills,
                                   salary_min=salary_min,
                                   salary_max=salary_max,
                                   description=description,
                                   company=company)
            is_updated = True
            return render(request, "jobs/vacancy-create.html", context={'form': form, 'is_updated': is_updated})
        else:
            is_updated = False
            return render(request, "jobs/vacancy-create.html", context={'form': form, 'is_updated': is_updated})


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
        if not request.user.is_authenticated:
            return redirect('/')
        if hasattr(request.user, 'company'):
            company = request.user.company
            initial_data = {"name": company.name, "location": company.location, "description": company.description,
                            "employee_count": company.employee_count, 'logo': company.logo}
            form = EditCompanyForm(request.POST or None, initial=initial_data)
            return render(request, "jobs/company-edit.html", context={"form": form})
        else:
            form = CompanyForm(request.POST or None)
            return render(request, "jobs/company-edit.html", context={"form": form})

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('/')
        if hasattr(request.user, 'company'):
            company = request.user.company
            form = EditCompanyForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                data = form.cleaned_data
                data.update({"user": request.user})
                print(data["logo"])
                if data['logo'] != None:
                    company.logo = data["logo"]
                company.name = data["name"]
                company.location = data["location"]
                company.description = data["description"]
                company.employee_count = data["employee_count"]
                company.save()
                is_updated = True
                return render(request, "jobs/company-edit.html", context={"form": form, 'is_updated': is_updated})
            else:
                is_updated = False
                return render(request, "jobs/company-edit.html", context={"form": form, 'is_updated': is_updated})
        else:
            form = CompanyForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                data = form.cleaned_data
                data.update({"user": request.user})
                Company.objects.create(**data)
            is_created = True
            return render(request, "jobs/company-edit.html", context={"form": form, 'is_created': is_created})


class MyLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True


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
            if hasattr(request.user, 'resume'):
                resume = request.user.resume
                initial_data = {"name": request.user.first_name,
                                "surname": request.user.last_name,
                                'status': resume.status,
                                'salary': resume.salary,
                                'speciality': resume.specialty,
                                'grade': resume.grade,
                                'education': resume.education,
                                'experience': resume.experience,
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
        if not request.user.is_authenticated:
            return redirect('/')
        form = ResumeForm(request.POST or None)
        if not form.is_valid():
            return render(request, "jobs/resume-edit.html", context={'form': form})
        data = form.cleaned_data
        user = request.user
        user.first_name = data["name"]
        user.last_name = data["surname"]
        user.save()
        del data["name"]
        del data["surname"]
        if hasattr(request.user, 'resume'):
            Resume.objects.filter(id=request.user.resume.id).update(**data)
            is_updated = True
            return render(request, "jobs/resume-edit.html", context={'form': form, 'is_updated': is_updated})
        else:
            data.update({"user": request.user})
            Resume.objects.create(**data)
            is_created = True
            return render(request, "jobs/resume-edit.html", context={'form': form, 'is_created': is_created})


class SearchView(View):
    def post(self, request):
        form = SearchForm(request.POST or None)
        if form.is_valid():
            search = form.cleaned_data.get('search')
            vacancies = Vacancy.objects.all()
            search_list = []
            for i in range(len(vacancies)):
                if search in vacancies[i].title:
                    search_list.append(vacancies[i])
                if search in vacancies[i].skills:
                    search_list.append(vacancies[i])
                if search in vacancies[i].description:
                    search_list.append(vacancies[i])
            return render(request, "jobs/search.html", context={'vacancies': search_list, 'search':search})
        else:
            return redirect('/')

def view_404 (request, exception):
    return render(
        request, '404.html'
    )


class ApplicationDeleteView(View):
    def get(self, request, id):
        application = Application.objects.filter(id=id).first()
        vacancy = application.vacancy
        application.delete()
        return redirect('/vacancy/edit/{}'.format(vacancy.id))
