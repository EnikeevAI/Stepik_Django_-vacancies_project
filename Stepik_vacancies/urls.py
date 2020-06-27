"""Stepik_vacancies URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path

from vacancies.views import CompanyView, ListOfVacanciesView, MainView, SendView, SpecializationView, \
    UserCompanyCreateView, UserCompanyVacanciesView, UserCompanyVacancyEditView, UserCompanyView, UserLoginView, \
    UserSignupView, VacancyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('companies/<int:id>', CompanyView.as_view()),
    path('mycompany/', UserCompanyView.as_view()),
    path('mycompany/create/', UserCompanyCreateView.as_view()),
    path('mycompany/vacancies/', UserCompanyVacanciesView.as_view()),
    path('mycompany/vacancies/<int:vacancy_id>', UserCompanyVacancyEditView.as_view()),
    path('vacancies/', ListOfVacanciesView.as_view()),
    path('vacancies/<int:vacancy_id>', VacancyView.as_view()),
    path('vacancies/<int:vacancy_id>/send/', SendView.as_view()),
    path('vacancies/cat/<str:cat>', SpecializationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('register/', UserSignupView.as_view())
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
