from urllib import request
from django.contrib.auth import *
from django.http import *
from django.shortcuts import *
from django.http.request import *
from django.core import serializers as CoreSerializers
from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User
from rest_framework import status, viewsets, renderers
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import *
from rest_framework.exceptions import ParseError
from rest_framework.generics import *
from rest_framework.parsers import *
from rest_framework.permissions import *
from rest_framework.response import *
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

from myApp.serializers import *

import json
import datetime, calendar

from decimal import *

date = datetime.date
today = datetime.datetime.today()
root = 'http://127.0.0.1:8000'


# my parsers
class MyJSONParser(BaseParser):
    media_type = 'application/json'
    renderer_class = renderers.JSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        request = parser_context.get('request')
        try:
            data = stream.read().decode(encoding)
            setattr(request, 'raw_body', data)  # setting a 'body' alike custom attr with raw POST content
            return json.loads(data)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))


class MyFORMParser(BaseParser):
    media_type = 'application/x-www-form-urlencoded'
    renderer_class = renderers.JSONRenderer

    def parse(self, stream, media_type=None, parser_context=None):
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)
        request = parser_context.get('request')
        try:
            data = stream.read().decode(encoding)
            setattr(request, 'raw_body', data)  # setting a 'body' alike custom attr with raw POST content
            return json.loads(data)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))


# @api_view(["POST"])
def Adminlogin(request):
    post = json.loads(request.body.decode('utf-8'))
    username = post.get("username")
    password = post.get("password")
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        data = {
            'status': True,
            'msg': 'Logged in'
        }
        return JsonResponse(data)
    else:
        data = {
            'status': False,
            'msg': 'Loggin Failed'
        }
        return JsonResponse(data)


def profileUpdate(request):
    post = json.loads(request.body.decode('utf-8'))
    user_id = post.get("user_id")
    firstname = post.get("firstname")
    lastname = post.get("lastname")
    email = post.get("email")
    address = post.get("address")
    city = post.get("city")
    country = post.get("country")
    zip_code = post.get("zip_code")

    userInstance = User.objects.get(id=user_id)
    userInstance.email = email
    userInstance.first_name = firstname
    userInstance.last_name = lastname
    profile = Profile.objects.filter(user=user_id)
    if profile.count == 1:
        instance = Profile.objects.filter(user=user_id)
        instance.address = address
        instance.city = city
        instance.country = country
        instance.zip_code = zip_code
        userInstance.save()
        instance.update()
        data = {
            'status': True,
            'msg': 'Successfull'
        }

    else:
        userInstance.save()
        instance = Profile(user=userInstance, address=address, city=city, country=country, zip_code=zip_code)
        instance.save()
        data = {
            'status': True,
            'msg': 'Successfull'
        }

    return JsonResponse(data)


def AdminLogout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect(root)
    else:
        return redirect(root)


@api_view(['GET', 'POST'])
def AddEmployee(request):
    if request.method == 'POST':
        post = request.data
        username = post.get("email")
        password = make_password(post.get("password"))
        first_name = post.get("first_name")
        last_name = post.get("last_name")
        email = post.get("email")
        address = post.get("address")
        city = post.get("city")
        country = post.get("country")
        zip_code = post.get("zip_code")

        user = UserSerializer(
            data={'username': username, 'password': password, 'first_name': first_name, 'last_name': last_name,
                  'email': email, 'is_active': True, 'is_staff': True})

        if user.is_valid():
            user.save()
            user_id = user.save().id
            profile = ProfileSerializer(
                data={'user': user_id, 'address': address, 'city': city, 'country': country, 'zip_code': zip_code})
            if profile.is_valid():
                profile.save()
                data = {
                    'status': True,
                    'msg': 'Success!'
                }
            else:
                data = {
                    'status': False,
                    'msg': 'Profile Save Failed'
                }
        else:
            data = {
                'status': False,
                'msg': 'Faled To Add Employee',
                'error': user.errors,
                'data': post,
            }
        return JsonResponse(data)


@api_view(['GET', 'POST'])
@parser_classes((JSONParser,))
def addSalary(request):
    if request.method == "POST":
        # post = json.loads(request.body.decode('utf-8'))
        post = request.data

        user = post.get('user')
        salary_amount = post.get('salary_amount')
        data = {'user': user, 'salary_amount': salary_amount}
        # return JsonResponse(data)
        serializer = SalarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = {
                'status': True,
                'msg': 'Success!'
            }
        else:
            data = {
                'status': False,
                'msg': 'Salary Add Failed',
                'error': serializer.errors
            }
    else:
        data = {
            'status': False,
            'msg': 'Faled To Add Salary',
        }
    return JsonResponse(data)


@api_view(['POST'])
def AttendenceSubmit(request):
    if request.method == "POST":
        post = request.data
        user = post.get('user')
        day = post.get('day')
        month = post.get('month')
        year = post.get('year')
        attendence_date = date(int(year), int(month), int(day))
        serializer = AttendenceSerializer(data={'user': user, 'status': True, 'attendence_date': attendence_date})
        count = Attendence.objects.filter(user=user, attendence_date__exact=date(year=int(year), month=int(month),
                                                                                 day=int(day))).count()
        if count < 1:
            if serializer.is_valid():
                serializer.save()
                data = {
                    'status': True,
                    'msg': 'Attendence Successfull',
                }
            else:
                data = {
                    'status': False,
                    'msg': 'Attendence Failed',
                    'error': serializer.errors
                }
        else:
            data = {
                'status': False,
                'msg': 'Attendence Failed'
            }
        return JsonResponse(data)


@api_view(['POST'])
def AttendenceChange(request):
    if request.method == "POST":
        post = request.data
        user = post.get('user')
        day = post.get('day')
        month = post.get('month')
        year = post.get('year')
        status = int(post.get('status'))
        attendence_date = date(int(year), int(month), int(day))
        data = {'user': user, 'status': status, 'attendence_date': attendence_date}
        count = Attendence.objects.filter(user=user, attendence_date__exact=date(year=int(year), month=int(month),
                                                                                 day=int(day))).count()
        if count == 1:
            attendence = Attendence.objects.filter(user=user,
                                                   attendence_date__exact=date(year=int(year), month=int(month),
                                                                               day=int(day))).update(status=status)
            data = {
                'success': True,
                'status': status,
                'msg': 'Attendence Updated',
            }
        elif count < 1:

            serializer = AttendenceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    'success': True,
                    'status': serializer.save().status,
                    'msg': 'Attendence Added',
                }
            else:
                data = {
                    'success': False,
                    'msg': 'Attendence Add Failed',
                    'error': serializer.errors
                }
        else:
            data = {
                'success': False,
                'msg': 'Failed',
                'count': count,
            }
        return JsonResponse(data)
