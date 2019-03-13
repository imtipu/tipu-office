from django.core import serializers
from django.shortcuts import *
from django.http import *
from django.contrib.auth import *
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.sessions.backends.db import SessionStore
from django.views.generic import *
from myApp.models import *
from .forms import *
import calendar
import datetime

root = '/'


def login(request):
    if not request.user.is_authenticated:
        data = {
            'title': 'Login'
        }
        return render(request, 'login.html', data)
    else:
        return redirect(root)


def home(request):
    if not request.user.is_authenticated:
        return redirect(root + 'login/')
    else:
        data = {
            'title': 'Home'
        }
        return render(request, 'home.html', data)


def AdminProfile(request, pk):
    try:
        profile = Profile.objects.get(user=pk)
    except Profile.DoesNotExist:
        profile = None
    data = {
        'title': request.user.username,
    }
    return render(request, 'profile.html', data)


class EmployeeList(ListView):
    model = User
    context_object_name = 'profiles'
    template_name = 'list_employee.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Employee List'
        return data


def AddNewEmployee(request):
    data = {
        'title': 'Add New Employee'
    }
    return render(request, 'add_employee.html', data)


class SalaryList(ListView):
    model = SalaryByUser
    context_object_name = 'salaries'
    template_name = 'salary_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(**kwargs)
        data['title'] = 'Salary List'
        return data


def AttendenceListUser(request):
    users = User.objects.filter(is_staff=True, is_active=True)
    data = {
        'title': 'Attendence',
        'users': users
    }
    return render(request, 'attendence_list_users.html', data)


def AttendencePage(request):
    today = datetime.datetime.today()
    thismonth = calendar.month(themonth=today.month, theyear=today.year)
    limit = str(today.month + 1)
    data = {
        'title': 'Attendence',
        'months': calendar.month_name,
        'days': thismonth,
        'this_month': today.month,
        'limit': ":" + limit
    }
    return render(request, 'attendence.html', data)


def AttendenceListByUser(request, pk):
    objects = Attendence.objects.filter(user=pk)
    user = User.objects.get(pk=pk)
    today = datetime.datetime.today()
    year = today.year
    month = today.month
    num_days = calendar.monthrange(year=year, month=month)[1]
    dates = list(range(0, num_days))
    limit = str(today.day + 1)
    data = {
        'lists': objects,
        'user': user,
        'title': user.first_name + ' Attendence',
        'dates': dates,
        'limit': ":" + limit,
    }
    return render(request, 'attendence_by_user.html', data)


## get forms

def getEmployeEditModal(request, pk):
    user = User.objects.get(pk=pk)
    data = {
        'user': User.objects.get(pk=pk),
        'form': UserForm(instance=user)
    }
    return render(request, 'get/modalEmployeEdit.html', data)


def salaryAddModalForm(request):
    users = User.objects.filter()
    data = {
        'users': users,
        'form': SalaryForm()
    }
    return render(request, 'get/salaryAddModal.html', data)
