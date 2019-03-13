from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import get_current_timezone, make_aware, utc, now


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    address = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=32, blank=True)
    country = models.CharField(max_length=32, blank=True)
    zip_code = models.CharField(max_length=6, blank=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profile'


class SalaryByUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    salary_amount = models.DecimalField(decimal_places=2, max_digits=10, default=None, blank=True, )
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'salary_by_user'


class Attendence(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    status = models.BooleanField(default=False, blank=True, null=True)
    attendence_date = models.DateField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendence'
