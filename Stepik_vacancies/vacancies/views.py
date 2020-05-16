from django.shortcuts import render
from django.views import View

from vacancies.models import Company, Specialty, Vacancy


class MainView(View):
    def get(self, request, *args, **kwargs):
        specialty_dict = dict()
        company_dict = dict()
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        for specialty in specialties:
            vacancies = Vacancy.objects.filter(specialty=specialty)
            specialty_dict[specialty.code] = vacancies
        for company in companies:
            vacancies = Vacancy.objects.filter(company=company)
            company_dict[company.name] = vacancies
        return render(
            request, 'vacancies/index.html',
            context={
                'specialties': specialties,
                'companies': companies,
                'specialty_dict': specialty_dict,
                'company_dict': company_dict
            }
            )


class ListOfVacanciesView(View):
    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        return render(
            request, 'vacancies/vacancies.html',
            context={
                'vacancies': vacancies
            }
        )


class SpecializationView(View):
    def get(self, request, *args, **kwargs):
        specialty_name = kwargs['cat']
        specialty = Specialty.objects.get(code=specialty_name)
        vacancies = Vacancy.objects.filter(specialty=specialty)
        return render(
            request, 'vacancies/vacancies.html',
            context={
                'vacancies': vacancies,
                'specialty': specialty
            }
        )


class CompanyView(View):
    def get(self, request, *args, **kwargs):
        company_id = kwargs['id']
        company = Company.objects.get(id=company_id)
        vacancies = Vacancy.objects.filter(company=company)
        return render(
            request, 'vacancies/company.html',
            context={
                'company': company,
                'vacancies': vacancies
            }
        )


class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        vacancy_id = kwargs['id']
        vacancy = Vacancy.objects.get(id=vacancy_id)
        return render(
            request, 'vacancies/vacancy.html',
            context={
                'vacancy': vacancy
            }
        )
