from django import forms


class ApplicationForm(forms.Form):
    written_username = forms.CharField(min_length=3, max_length=50, label='Name and Surname', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                   'id': 'userName',
                                                                                   'placeholder': 'Name',
                                                                                   'required': True}))
    written_phone = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'required': True,
                                                                                'placeholder': 'Phone',
                                                                                'id': 'userPhone'}))
    written_cover_letter = forms.CharField(min_length=3, max_length=550, label='message', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                               'required': True,
                                                                               'id': 'userMsg',
                                                                               'rows':"8"}))

    def clean_phone(self):
        number = self.cleaned_data.get("phone")
        if number[0] != '+':
            # return self.add_error('phone','You have to set "+" first')
            raise forms.ValidationError('You have to set "+" first')
        return number


class VacancyForm(forms.Form):
    title = forms.CharField(min_length=3, max_length=50, label='Title', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                   'id': 'vacancyTitle',
                                                                                   'placeholder': 'Title',
                                                                                   'required': True}))
    speciality = forms.ChoiceField(widget=forms.Select(attrs={'class': 'custom-select mr-sm-2',
                                                         'id': 'userSpecialization',
                                                         'required': True}), choices=[('frontend', 'Фронтенд'),
                                                             ('backend', 'Бекенд'),
                                                             ('gamedev', 'Геймдев'),
                                                             ('devops', 'Девопс'),
                                                             ('products', 'Продукты'),
                                                             ('management', 'Менеджмент'),
                                                             ('testing', 'Тестирование'),
                                                             ('design', 'Дизайн'),])
    salary_min = forms.IntegerField(min_value=100, label='Min salary',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'id': 'vacancySalaryMin',
                                                           'placeholder': 'Minimal Salary',
                                                           'required': True}))
    salary_max = forms.IntegerField(min_value=200, label='Max salary',
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'id': 'vacancySalaryMax',
                                                                   'placeholder': 'Maximal salary',
                                                                   'required': True}))
    description = forms.CharField(min_length=10, max_length=550, label='description', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                               'required': True,
                                                                               'id': 'userMsg',
                                                                                'placeholder': 'Description',
                                                                               'rows':"8"}))
    skills = forms.CharField(min_length=3, max_length=550, label='skills', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                 'required': True,
                                                                                'placeholder': 'Skils',
                                                                                 'id': 'vacancySkills',
                                                                                 'rows': "3"}))


    def clean_salary_max(self):
        salary_min = self.cleaned_data.get("salary_min")
        salary_max = self.cleaned_data.get("salary_max")
        if salary_min > salary_max:
            raise forms.ValidationError("Minimal salary can't be more than maximal salary")
        return salary_max


class CompanyForm(forms.Form):
    name = forms.CharField(min_length=3, max_length=64, label='Name', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                        'id': 'companyName',
                                                                                        'placeholder': 'Company name',
                                                                                        'required': True}))
    location = forms.CharField(min_length=3, max_length=64, label='Location', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                        'id': 'companyLocation',
                                                                                        'placeholder': 'Company location',
                                                                                        'required': True}))
    logo = forms.FileField(label='Download', required=True, widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
    employee_count = forms.IntegerField(label='Employee count',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'companyTeam',
                                                         'placeholder': '1',
                                                         'required': True}))
    description = forms.CharField(label='Description', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                    'required': True,
                                                                                    'id': 'companyInfo',
                                                                                    'placeholder': 'Description',
                                                                                    'rows': "8"}))


class ResumeForm(forms.Form):
    status = forms.ChoiceField(widget=forms.Select(attrs={'class': 'custom-select mr-sm-2',
                                                         'id': 'userReady',
                                                         'required': True}), choices=[('Ищу работу', 'Ищу работу'),
                                                             ('Открыт к предложениям', 'Открыт к предложениям'),
                                                             ('Не ищу работу', 'Не ищу работу'),])
    portfolio = forms.CharField(min_length=5, max_length=250, label='Portfolio',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'userPortfolio',
                                                         'placeholder': 'Portfolio',
                                                         'required': True}))
    speciality = forms.ChoiceField(widget=forms.Select(attrs={'class': 'custom-select mr-sm-2',
                                                              'id': 'userPortfolio',
                                                              'required': True}), choices=[('frontend', 'Фронтенд'),
                                                                                           ('backend', 'Бекенд'),
                                                                                           ('gamedev', 'Геймдев'),
                                                                                           ('devops', 'Девопс'),
                                                                                           ('products', 'Продукты'),
                                                                                           ('management', 'Менеджмент'),
                                                                                           ('testing', 'Тестирование'),
                                                                                           ('design', 'Дизайн'), ])
    grade = forms.ChoiceField(widget=forms.Select(attrs={'class': 'custom-select mr-sm-2',
                                                              'id': 'userQualification',
                                                              'required': True}), choices=[('junior', 'Младший (junior)'),
                                                                                           ('middle', 'Средний (middle)'),
                                                                                           ('senior', 'Старший (senior)'),
                                                                                            ])
    salary = forms.IntegerField(label='Salary',
                                    widget=forms.TextInput(attrs={'class': 'form-control',
                                                                  'id': 'userSalary',
                                                                  'placeholder': 'Salary',
                                                                  'required': True}))
    education = forms.CharField(min_length=5, max_length=250, label='Education', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                    'required': True,
                                                                                    'id': 'userEducation',
                                                                                    'placeholder': 'Education',
                                                                                    'rows': "4"}))
    experience = forms.CharField(min_length=5, max_length=250, label='Experience', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                    'required': True,
                                                                                    'id': 'userExperience',
                                                                                    'placeholder': 'Experience',
                                                                                    'rows': "4"}))
    name = forms.CharField(min_length=3, max_length=50, label='Name',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'Name',
                                                         'placeholder': 'Name',
                                                         'required': True}))
    surname = forms.CharField(min_length=3, max_length=50, label='Surname',
                           widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'id': 'Surname',
                                                         'placeholder': 'Surname',
                                                         'required': True}))


class SearchForm(forms.Form):
    search = forms.CharField(min_length=3, max_length=50, label='Search',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                              'placeholder': 'Search for the vacancies',
                                                              'required': True,
                                                              'class': 'form-control w-100',
                                                              'type':'search',
                                                              'aria-label': 'Search for the vacancies'}))