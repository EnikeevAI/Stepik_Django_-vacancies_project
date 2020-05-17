import random

from django.core.management.base import BaseCommand

from vacancies.data import companies, jobs, specialties
from vacancies.models import Company, Specialty, Vacancy


class Command(BaseCommand):
    def add_company_table_dbdata(self, companies=companies, Company=Company):
        for company in companies:
            Company.objects.create(
                name=company['title'],
                location=f"{company['title']} location",
                logo=f"static/company_logo/{company['logo']}",
                description=f"{company['title']} description",
                employee_count=random.randint(1, 10)
            )

    def add_specialty_table_dbdata(self, specialties=specialties, Specialty=Specialty):
        for speciality in specialties:
            Specialty.objects.create(
                code=speciality['code'],
                title=speciality['title'],
                picture=f"static/specialities_logo/specty_{speciality['code']}.png"
            )

    def add_vacancy_table_dbdata(self, jobs=jobs, Vacancy=Vacancy, Company=Company, Specialty=Specialty):
        for job in jobs:
            company = Company.objects.filter(name=job['company']).first()
            speciality = Specialty.objects.filter(code=job['cat']).first()
            Vacancy.objects.create(
                title=job['title'],
                specialty=speciality,
                company=company,
                skills=f"{job['title']} skills",
                description=job['desc'],
                salary_min=job['salary_from'],
                salary_max=job['salary_to'],
                published_at=job['posted']
            )

    def add_data_to_db(self):
        self.add_company_table_dbdata()
        self.add_specialty_table_dbdata()
        self.add_vacancy_table_dbdata()

    def handle(self, *args, **kwargs):
        self.add_data_to_db()
        print("Data added")
