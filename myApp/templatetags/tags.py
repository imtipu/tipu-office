from django import template

register = template.Library()
from myApp.models import *
import datetime

today = datetime.datetime.today()
date = datetime.date


@register.filter
def addString(arg1, arg2):
    return str(arg1) + str(arg2)


@register.simple_tag()
def get_attedence_status(user, day, month, year):
    attendence = Attendence.objects.filter(user=user, attendence_date__exact=date(year=int(year), month=int(month),
                                                                                  day=int(day))).first()
    data = {
        'day': int(day),
        'day_today': int(today.day),
        'month': int(month),
        'year': int(year),
        'attendence': attendence
    }
    return data


@register.simple_tag()
def get_today_attendence(user, day, month, year):
    attendence = Attendence.objects.filter(user=user, attendence_date__exact=date(year=int(year), month=int(month),
                                                                                  day=int(day))).first()
    return attendence
