from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from vacancies.models import Application, Company, Specialty, Vacancy
from vacancies.forms import UserApplicationForm, UserAuthenticationForm, UserRegisterForm

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


class UserRegisterView(CreateView):
   form_class = UserCreationForm
   success_url = 'login'
   template_name = 'vacancies/register.html'


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


class SendView(View):
    template_name = 'vacancies/sent.html'

    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        return render(
            request, self.template_name,
            context={
                'vacancy': vacancy,
            }
        )


class VacancyView(View):
    template_name = 'vacancies/vacancy.html'

    def get_current_user(self, request):
        return request.user if request.user.is_authenticated else None

    def get_vacancy(self, vacancy_id):
        try:
            vacancy = Vacancy.objects.get(id=vacancy_id)
        except Vacancy.DoesNotExist:
            raise Http404(f"Vacancy with id={vacancy_id} not exist")
        return vacancy

    def get(self, request, vacancy_id, *args, **kwargs):
        form = UserApplicationForm()
        user = self.get_current_user(request)
        vacancy = self.get_vacancy(vacancy_id)
        return render(
            request, self.template_name,
            context={
                'form': form,
                'vacancy': vacancy,
                'user': user
            }
        )

    def post(self, request, vacancy_id):
        form = UserApplicationForm(request.POST)
        user = self.get_current_user(request)
        vacancy = self.get_vacancy(vacancy_id)
        if form.is_valid() and user is not None:
            username = form.cleaned_data['username']
            userphone = form.cleaned_data['userphone']
            usermsg =  form.cleaned_data['usermsg']
            Application.objects.create(
                written_username=username,
                written_phone=userphone,
                written_cover_letter=usermsg,
                vacancy=vacancy,
                user=user
            )
            return redirect(f'/vacancies/{vacancy_id}/send/')

        return render(
            request, self.template_name,
            context={
                'form': form,
                'vacancy': vacancy,
                'user': user
            }
        )


class UserLoginView(LoginView):
    redirect_authenticated_user = True
    authentication_form = UserAuthenticationForm
    template_name = 'vacancies/login.html'


class UserSignupView(LoginView):
    template_name = 'vacancies/register.html'

    def get(self, request):
        form = UserRegisterForm()
        return render(
            request, self.template_name,
            context={
                'form': form
            }
        )

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=password
            )
            user.save()
            return redirect('/login/')
        return render(
            request, self.template_name,
            context={
                'form': form
            }
        )
