"""BankSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path
from Search import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', views.index),
    path('index/',views.index),
    path('statistic/', views.teacher_statistic),

    path('project/search/', views.project_search),
    path('project/insert/', views.project_insert),
    path('project/get_teacher_name/', views.get_teacher_name, name='get_teacher_name'),
    re_path(r'^project/[A-Z0-9]{5}/update', views.project_update),

    path('paper/search/', views.paper_search),
    path('paper/insert/', views.paper_insert),
    path('paper/get_teacher_name/', views.get_teacher_name, name='get_teacher_name'),
    re_path(r'^paper/\d{1,4}/update$', views.paper_update),

    # re_path(r'^project/[A-Z0-9]{4}/delete/$', views.project_delete),


    # path('client/insert/', views.client_insert),
    # re_path(r'^client/[A-Z0-9]{4}/update/$', views.client_update),
    # path('client/search/',views.client_search),

    # path('account/search/',views.account_search),
    # path('account/insert_checking/', views.account_insert_checking),
    # path('account/insert_saving/', views.account_insert_saving),
    # re_path(r'^account/[A-Z0-9]{4}/update/$', views.account_update),

    # path('loan/search/',views.loan_search),
    # path('loan/insert/', views.loan_insert),
    # re_path(r'^loan/insert/[A-Z0-9]{4}/$', views.client_loan),
    # re_path(r'^loan/[A-Z0-9]{4}/issue/$', views.loan_issue),

]
