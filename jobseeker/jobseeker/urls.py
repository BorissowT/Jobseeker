from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path

from jobs.views import MainView, VacanciesView, CategoryView, CompanyView, MyLoginView, MySignupView, ResumeView, ResumeCreateView, MyCompanyView, MyCompanyEditView, VacancyView, CompaniesView, VacancyEditView


urlpatterns = [
    path('', MainView.as_view(), name="main"),

    # path('jobs/<int:id>/send/', SendView.as_view()),
    path('category/<str:category>/', CategoryView.as_view(), name="category"),

    path('admin/', admin.site.urls, name="admin")
]

urlpatterns += [
    path('vacancies/', VacanciesView.as_view(), name="vacancies"),
    path('vacancy/<int:id>', VacancyView.as_view(), name="vacancy"),
    path('vacancy/edit/<int:id>', VacancyEditView.as_view(), name="vacancy/edit"),
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