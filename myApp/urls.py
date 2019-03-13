from django.urls import path
from myApp import views, api

urlpatterns = [
    path('', views.home, name="homepage"),
    path('login/', views.login),
    path('dashboard/admin/<int:pk>/profile/', views.AdminProfile, name="admin_profile"),
    path('dashboard/list-employee/', views.EmployeeList.as_view(), name="list_employee"),
    path('dashboard/add-employee/', views.AddNewEmployee, name="add_employee"),

    ## path('dashboard/'),
    path('dashboard/salary-list/', views.SalaryList.as_view(), name="salary_list"),
    path('dashboard/attendence-user-list/', views.AttendenceListUser, name="attendence_list_users"),
    path('dashboard/attendence/', views.AttendencePage, name="attendence_list"),
    path('dashboard/attendence/<int:pk>/', views.AttendenceListByUser, name="attendence_list_user"),
    ## api urls
    path('api/login/', api.Adminlogin, name="admin_login"),
    path('api/profileUpdate/', api.profileUpdate, name="profileUpdate"),
    path('api/logout/', api.AdminLogout, name="admin_logout"),
    path('api/add-employee/', api.AddEmployee, name="api_add_employee"),
    path('api/add-salary/', api.addSalary, name="api_add_salary"),
    path('api/add-today-attendence/', api.AttendenceSubmit, name="api_attendence_submit"),
    path('api/attendence-change/', api.AttendenceChange, name="api_attendence_change"),
    # get forms
    path('get/forms/employeeEditModalForm/<int:pk>/', views.getEmployeEditModal, name="employeeEditModal"),
    path('get/forms/salaryAddModalForm/', views.salaryAddModalForm, name="salaryAddModal"),

]
