from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.urls import re_path
from django.views.static import serve
from jobs.views import *

urlpatterns = [
    path('', MainView.as_view(), name="main"),
    path('search/', SearchView.as_view(), name='search'),

    path('category/<str:category>/', CategoryView.as_view(), name="category"),
    path('application/delete/<int:id>', ApplicationDeleteView.as_view(), name="delete"),
    path('admin/', admin.site.urls, name="admin")
]

urlpatterns += [
    path('vacancies/', VacanciesView.as_view(), name="vacancies"),
    path('vacancy/<int:id>', VacancyView.as_view(), name="vacancy"),
    path('vacancy/edit/<int:id>', VacancyEditView.as_view(), name="vacancy/edit"),
    path('vacancy/create', VacancyCreateView.as_view(), name="vacancy/create")
]

urlpatterns += [
    path('company/<int:id>/', CompanyView.as_view(), name="company"),
    path('mycompany/', MyCompanyView.as_view(), name="mycompany"),
    path('mycompany/edit', MyCompanyEditView.as_view(), name="mycompany/edit"),
    path('companies/', CompaniesView.as_view(), name="companies"),
]

urlpatterns += [
    path('myresume', ResumeView.as_view(), name="myresume"),
    path('myresume/edit', ResumeCreateView.as_view(), name="myresume/edit"),
]

urlpatterns += [
    path('login/', MyLoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
    path('signup', MySignupView.as_view(), name="signup")
]

urlpatterns += [
    re_path(r'^media/(?P<path>.*)$',
    serve,
    {'document_root': settings.MEDIA_ROOT})
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = 'jobs.views.view_404'