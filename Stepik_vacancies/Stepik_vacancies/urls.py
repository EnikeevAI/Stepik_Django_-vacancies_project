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
from django.contrib import admin
from django.urls import path
from vacancies.views import MainView, ListOfVacanciesView, SpecializationView, CompanyView, VacanciesView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view()),
    path('companies/<int:id>', CompanyView.as_view()),
    path('vacancies/', ListOfVacanciesView.as_view()),
    path('vacancies/<int:id>', VacanciesView.as_view()),
    path('vacancies/cat/<str:cat>', SpecializationView.as_view()),
]
