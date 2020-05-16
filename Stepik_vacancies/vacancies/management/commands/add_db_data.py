from django.db import models

from data import companies, jobs, specialties
from models import Company, Specialty, Vacancy


def add_company_table_dbdata(companies):
    for company in companies:
        company_db = Company(
            name=company['title']
        )