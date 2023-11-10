from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
import pandas as pd
import numpy as np
from datetime import datetime as dtt
from django.utils import timezone
import datetime

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import  csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.contrib.auth.models import Group

# Database Connections
from django.db import connections
from django.http import JsonResponse
from django.conf import settings


# import models and Forms
from .forms import ClientsForm, SiteConfigForm
from .models import Clients,SiteConfig,ClientPlans,Plans, VDbApi
from .serializers import VBADataSerializer
from rest_framework.renderers import JSONRenderer

# datetime.datetime.now(tz=timezone.utc) # you can use this value


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser or u.role_type == 'ADMIN', login_url='403')
def admin_home(request):
    clients = Clients.objects.filter(role_type='CLIENT').values()
    sites = SiteConfig.objects.all().values()
    plans = Plans.objects.all().values()
    client_plans = ClientPlans.objects.all().values()

    context = {'clients':clients,'sites':sites,'plans':plans,'client_plans':client_plans}
    return render(request=request,template_name='apis/admin_home.html',context=context)


@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser or u.role_type == 'ADMIN', login_url='403')
def add_site(request):
    form = SiteConfigForm()
    if request.method == 'POST':
        form = SiteConfigForm(request.POST, request.FILES)
        if form.is_valid():
            name = request.POST['site_name']
            form.save()        
            messages.success(request,f"Site Added {name}")
            return redirect('add_site')
        else:
            messages.error(request,"There was an error in the form")
    context = {'site_form':form}
    return render(request=request,template_name='apis/add_site.html',context=context)

# Create your views here.
@csrf_protect
def admin_login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("sample_page")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    context = {'admin_form': form}
    return render(request, template_name='apis/admin_login.html', context=context)


def sample_page(request):
    return render(request=request,template_name='apis/admin_login.html',context={})

@login_required(login_url='admin_login')
@user_passes_test(lambda u: u.is_superuser or u.role_type == 'ADMIN', login_url='403')
def create_client(request):
    form = ClientsForm()
    if request.method == "POST":
        form = ClientsForm(request.POST, request.FILES)
        if form.is_valid():
            group_data = form.cleaned_data['role_type']
            # print(form.cleaned_data['role_type'])
            user = form.save()
            # Save admins to admin group
            client_group = Group.objects.get(name='Client')
            admin_group = Group.objects.get(name='Admin')
            if group_data == "CLIENT":
                user.groups.add(client_group)
            elif client_group == "ADMIN":
                user.groups.add(admin_group)
                list_perms = ['Can add user', 'Can change user', 'Can delete user', 'Can view user']
                for x in list_perms:
                    permission = Permission.objects.get(name=x)
                    user.user_permissions.add(permission)
            messages.success(request, "Client Successfully Added")
            return redirect('create_client')
        else:
            messages.warning(request, "There was an error in the Form")
    context = {'form': form}
    return render(request=request,template_name='apis/create_client.html',context=context)


def custom_403_view(request, exception=None):
    return render(request, 'apis/403.html', status=403)

@csrf_protect
def client_login(request):
    pass

@login_required
def client_homepage(request):
    pass



@login_required(login_url='admin_login')
def premium(request):
    user = request.user
    user_name = request.user.username
    plan_id = user.plans_id
    # print(user.plans_id)
    if plan_id.lower() == "basic":
        return redirect('403')
    else:
        print("Premium")
    sites = list(SiteConfig.objects.filter(client_name = user_name).values_list('site_name',flat=True))
    date_now = dtt.now()
    now_api = VDbApi.objects.filter(site_name__in = sites,timestamp__gte = date_now ).values()
    data_serialize = VBADataSerializer(now_api,many=True)
    js_data = JSONRenderer().render(data_serialize.data)
    return render(request,template_name='apis/sample.html',context={'data':js_data})
