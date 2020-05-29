from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import redirect, render
from django.views import View

from vacancies.models import Application, Company, Specialty, Vacancy
from vacancies.forms import UserApplicationForm, UserAuthenticationForm, UserCompanyEditForm, \
    UserCompanyVacancyEditForm, UserRegisterForm


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
        try:
            specialty = Specialty.objects.get(code=cat)
        except Specialty.DoesNotExist:
            raise Http404(f'Company with cat "{cat}" not exist')
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
            form = form.save(commit=False)
            form.vacancy = vacancy
            form.user = user
            form.save()
            return redirect(f'/vacancies/{vacancy_id}/send/')

        return render(
            request, self.template_name,
            context={
                'form': form,
                'vacancy': vacancy,
                'user': user
            }
        )


class UserCompanyCreateView(View):
    template_name = 'vacancies/company_create.html'

    def get(self, request):
        return render(
            request, self.name, context={}
        )

    def post(self, request):
        user = User.objects.filter(username=request.user).first()
        Company.objects.create(
            name='Введите название компании',
            location='Введите местоположение компании',
            description='Введите описание компании',
            employee_count=1,
            logo=None,
            owner=user
        )
        return redirect('/mycompany/')


class UserCompanyView(View):
    template_name = 'vacancies/company_edit.html'
    model_changed = False

    def initializing_the_form_on_request(self, request):
        user = User.objects.filter(username=request.user).first()
        company = Company.objects.filter(owner=user).first()
        if request.method == 'GET':
            form = UserCompanyEditForm(instance=company)
        else:
            form = UserCompanyEditForm(request.POST, request.FILES, instance=company)
        return user, company, form

    def get(self, request):
        user, company, form = self.initializing_the_form_on_request(request)
        if company is None:
            return redirect('/mycompany/create/')
        return render(
            request, self.template_name,
            context={
                'form': form,
                'company': company,
                'model_changed': self.model_changed
            }
        )

    def post(self, request):
        user, company, form = self.initializing_the_form_on_request(request)
        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.owner = user
            post_form.save()
            self.model_changed = True
            return redirect('/mycompany/')
        else:
            form = UserCompanyEditForm(instance=company)
        return render(
            request, self.template_name,
            context={
                'form': form,
                'company': company,
                'model_changed': self.model_changed
            })


class UserCompanyVacanciesView(LoginView):
    template_name = 'vacancies/vacancy-list.html'

    def get(self, request):
        user = User.objects.filter(username=request.user).first()
        company = Company.objects.filter(owner=user).first()
        if company is None:
            return redirect('/mycompany/create/')
        vacancies = Vacancy.objects.filter(company=company).all()
        return render(
            request, self.template_name,
            context={
                'vacancies': vacancies
            }
        )


class UserCompanyVacancyEditView(LoginView):
    template_name = 'vacancies/vacancy-edit.html'
    model_changed = False

    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        user = User.objects.filter(username=request.user).first()
        company = Company.objects.filter(owner=user).first()
        if vacancy:
            form = UserCompanyVacancyEditForm(instance=vacancy)
        else:
            specialty = Specialty.objects.all().first()
            vacancy = Vacancy.objects.create(
                title='Введите название вакансии',
                company=company,
                skills='Введите требуемые навыки',
                description='Введите описание',
                salary_min=0,
                salary_max=0,
                specialty=specialty
            )
            form = UserCompanyVacancyEditForm(instance=vacancy)
        applications = Application.objects.filter(vacancy=vacancy).all()
        return render(
            request, self.template_name,
            context={
                'applications': applications,
                'company': company,
                'form': form,
                'model_changed': self.model_changed,
                'vacancy': vacancy
            }
        )

    def post(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        user = User.objects.filter(username=request.user).first()
        company = Company.objects.filter(owner=user).first()
        form = UserCompanyVacancyEditForm(request.POST, instance=vacancy)
        if form.is_valid():
            specialty = Specialty.objects.filter(title=request.POST['specialty']).first()
            post_form = form.save(commit=False)
            post_form.specialty = specialty
            post_form.company = company
            post_form.save()
            self.model_changed = True
        else:
            form = UserCompanyVacancyEditForm(instance=vacancy)
        applications = Application.objects.filter(vacancy=vacancy).all()
        return render(
            request, self.template_name,
            context={
                'applications': applications,
                'company': company,
                'form': form,
                'model_changed': self.model_changed,
                'vacancy': vacancy,
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
            form.save()
            return redirect('/login/')
        return render(
            request, self.template_name,
            context={
                'form': form
            }
        )
