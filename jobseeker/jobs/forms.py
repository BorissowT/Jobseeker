from django import forms
from django.forms.widgets import SelectDateWidget


class ApplicationForm(forms.Form):
    name = forms.CharField(label='Name and Surname', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                   'id': 'userName',
                                                                                   'placeholder': 'Name',
                                                                                   'required': True}))
    phone = forms.CharField(label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                'required': True,
                                                                                'placeholder': 'Phone',
                                                                                'id': 'userPhone'}))
    message = forms.CharField(label='message', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                               'required': True,
                                                                               'id': 'userMsg',
                                                                               'rows':"8"}))

    def clean_phone(self):
        number = self.cleaned_data.get("phone")
        if number[0] != '+':
            # return self.add_error('phone','You have to set "+" first')
            raise forms.ValidationError('You have to set "+" first')
        return number

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if len(name) < 2:
            raise forms.ValidationError('name','Please, type your name and surname')
        return name

    def cleaned_message(self):
        message = self.cleaned_data.get("message")
        if len(message) < 10:
            return self.add_error('message','Please, type your message to the employer')
        return message






class VacancyForm(forms.Form):
     title = forms.CharField(max_length=64, label='Title', widget=forms.TextInput(attrs={'class': 'form-control',
                                                                                   'id': 'vacancyTitle',
                                                                                   'placeholder': 'Title',
                                                                                   'required': True}))
     speciality = forms.CharField(max_length=64, label='Speciality',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Speciality',
                                                           'id': 'specialisation',
                                                           'required': True}))
     salary_min = forms.IntegerField(label='Min salary',
                             widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'id': 'vacancySalaryMin',
                                                           'placeholder': 'Minimal Salary',
                                                           'required': True}))
     salary_max = forms.IntegerField(label='Max salary',
                                     widget=forms.TextInput(attrs={'class': 'form-control',
                                                                   'id': 'vacancySalaryMax',
                                                                   'placeholder': 'Maximal salary',
                                                                   'required': True}))
     description = forms.CharField(label='description', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                               'required': True,
                                                                               'id': 'userMsg',
                                                                                'placeholder': 'Description',
                                                                               'rows':"8"}))
     skills = forms.CharField(label='skills', widget=forms.Textarea(attrs={'class': 'form-control',
                                                                                 'required': True,
                                                                                'placeholder': 'Skils',
                                                                                 'id': 'vacancySkills',
                                                                                 'rows': "3"}))

     def clean_title(self):
         title = self.cleaned_data.get("title")
         if len(title) < 2:
            raise forms.ValidationError('This field is required')
         return title

     def clean_speciality(self):
        specialisation = self.cleaned_data.get("speciality")
        if specialisation == "backend" or specialisation == "frontend"\
                or specialisation == "gamedev" \
                or specialisation == "devops"\
                or specialisation == "design"\
                or specialisation == "products" \
                or specialisation == "management"\
                or specialisation == "testing":
            return specialisation
        raise forms.ValidationError('There are only("gamedev","devops","design", "products", "management", "testing") specialities')

     def clean_description(self):
        description = self.cleaned_data.get("description")
        if len(description) < 10:
            raise forms.ValidationError('This field is required')
        return description

     def clean_skills(self):
        skills = self.cleaned_data.get("skills")
        if len(skills) < 10:
            raise forms.ValidationError('This field is required')
        return skills

     def clean_salary_min(self):
        salary_min = self.cleaned_data.get("salary_min")
        if salary_min < 0:
            raise forms.ValidationError("Salary can't be less than 0")
        return salary_min

     def clean_salary_max(self):
        salary_max = self.cleaned_data.get("salary_max")
        if salary_max < 0:
            raise forms.ValidationError("Salary can't be less than 0")
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
    logo = forms.FileField(label='Download', required=False,widget=forms.FileInput(attrs={'class': 'custom-file-input'}))
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
