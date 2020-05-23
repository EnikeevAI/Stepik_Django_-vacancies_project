from django.http import Http404
from django.shortcuts import render
from django.views import View

from vacancies.models import Company, Specialty, Vacancy


class MainView(View):
    def get(self, request, *args, **kwargs):
        specialties = Specialty.objects.all()
        companies = Company.objects.all()
        return render(
            request, 'vacancies/index.html',
            context={
                'specialties': specialties,
                'companies': companies
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
    def get(self, request, cat, *args, **kwargs):
        specialty_cat = cat
        try:
            specialty = Specialty.objects.get(code=specialty_cat)
        except Specialty.DoesNotExist:
            raise Http404(f'Company with cat "{specialty_cat}" not exist')
        vacancies = Vacancy.objects.filter(specialty=specialty)
        return render(
            request, 'vacancies/vacancies.html',
            context={
                'vacancies': vacancies,
                'specialty': specialty
            }
        )


class CompanyView(View):
    def get(self, request, id, *args, **kwargs):
        company_id = id
        try:
            company = Company.objects.get(id=company_id)
        except Company.DoesNotExist:
            raise Http404(f"Company with id={company_id} not exist")
        vacancies = Vacancy.objects.filter(company=company)
        return render(
            request, 'vacancies/company.html',
            context={
                'company': company,
                'vacancies': vacancies
            }
        )


class VacancyView(View):
    def get(self, request, id, *args, **kwargs):
        vacancy_id = id
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise Http404(f"Vacancy with id={vacancy_id} not exist")
        return render(
            request, 'vacancies/vacancy.html',
            context={
                'vacancy': vacancy
            }
        )
