from django import forms
from myApp.models import *
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'is_active',
            'is_staff',
            'is_superuser'
        )


class SalaryForm(forms.ModelForm):
    class Meta:
        model = SalaryByUser
        fields = (
            'user',
            'salary_amount'
        )
