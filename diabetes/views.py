from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InsulinInjection, Food, Bloodcheck
from jalali_date import date2jalali
from .forms import Bloodcheckform, InsulinFoodForm
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from itertools import chain
from collections import defaultdict

""" def my_view(request):
    jalali_join = date2jalali(
        request.user.date_joined).strftime('%y/%m/%d')
 """


@login_required
def bloodcheckView(request):
    if request.method == "POST":
        bloodcheckform = Bloodcheckform(request.POST, request.FILES)
        if bloodcheckform.is_valid():
            # Set the user to the logged-in user
            bloodcheck = bloodcheckform.save(commit=False)  # Don't save yet
            bloodcheck.user = request.user  # Set the logged-in user
            bloodcheck.save()  # Now save it
    else:
        bloodcheckform = Bloodcheckform()

    context = {
        'form': bloodcheckform
    }
    return render(request, "diabetes/bloodcheck.html", context)


@login_required
def bloodcheck_list(request):
    bloodchecks = Bloodcheck.objects.filter(
        user=request.user).order_by('-date', '-time')

    paginator = Paginator(bloodchecks, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    bloodchecks_list = []
    for check in page_obj:
        bloodchecks_list.append({
            'id': check.id,
            'bloodsugar': check.bloodsugar,
            'time': check.time.strftime("%H:%M"),
            'date': date2jalali(check.date).strftime("%Y/%m/%d"),
            'event': check.event,
        })

    context = {
        'bloodchecks': bloodchecks_list,
        'page_obj': page_obj,
    }
    return render(request, 'diabetes/bloodcheck_list.html', context)


@login_required
def insulin_food_entry(request):
    if request.method == "POST":
        form = InsulinFoodForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save(user=request.user)
            # Change to your desired redirect
            return redirect('bloodcheck_list')
    else:
        form = InsulinFoodForm(user=request.user)

    return render(request, 'diabetes/insulin_food_form.html', {'form': form})


@login_required
def insulin_food_list(request):
    insulin_injections = InsulinInjection.objects.filter(
        user=request.user).order_by('-date', '-time')
    food_entries = Food.objects.filter(
        user=request.user).order_by('-date', '-time')
    combined_entries = list(chain(insulin_injections, food_entries))
    combined_entries.sort(key=lambda x: (x.date, x.time), reverse=True)

    log_by_jalali_month = defaultdict(list)
    for entry in combined_entries:
        jalali_date = date2jalali(entry.date)
        jalali_month_year = jalali_date.strftime('%Y/%m')
        entry_data = {
            'id': entry.id,
            'type': entry.__class__.__name__,
            'time': entry.time.strftime("%H:%M"),
            'date': jalali_date.strftime("%Y/%m/%d"),
            'insulin_type': entry.insulin_type if isinstance(entry, InsulinInjection) else None,
            'insulin_dose': entry.insulin_dose if isinstance(entry, InsulinInjection) else None,
            'injection_site': entry.injection_site if isinstance(entry, InsulinInjection) else None,
            'food': entry.food if isinstance(entry, Food) else None,
            'carbs': entry.carbs if isinstance(entry, Food) else None,
        }
        log_by_jalali_month[jalali_month_year].append(entry_data)

    # Handle month selection from GET request
    selected_month = request.GET.get('month')
    if selected_month:
        try:
            year, month = map(int, selected_month.split('/'))
            jalali_filter = f"{year}/{month:02d}"
            filtered_log = {
                jalali_filter: log_by_jalali_month[jalali_filter]} if jalali_filter in log_by_jalali_month else {}
        except (ValueError, KeyError):
            filtered_log = dict(
                sorted(log_by_jalali_month.items(), reverse=True))
    else:
        filtered_log = dict(sorted(log_by_jalali_month.items(), reverse=True))

    available_months = sorted(log_by_jalali_month.keys(), reverse=True)
    context = {
        'log': filtered_log,
        'available_months': available_months,
        'selected_month': selected_month,
    }
    return render(request, 'diabetes/insulin_food_list.html', context)


def home(request):
    insulin_food_form = InsulinFoodForm(user=request.user)
    # Initialize both forms
    bloodcheck_form = Bloodcheckform()
    insulin_food_form = InsulinFoodForm(user=request.user)

    # Determine which form to show (default to bloodcheck)
    form_type = request.GET.get('form_type', 'bloodcheck')

    # Handle POST requests
    if request.method == "POST":
        if 'bloodcheck_submit' in request.POST:
            bloodcheck_form = Bloodcheckform(request.POST, request.FILES)
            if bloodcheck_form.is_valid():
                bloodcheck = bloodcheck_form.save(commit=False)
                bloodcheck.user = request.user
                bloodcheck.save()
                return redirect('home')  # Refresh home page after save
        elif 'insulin_food_submit' in request.POST:
            insulin_food_form = InsulinFoodForm(
                user=request.user, data=request.POST)
            if insulin_food_form.is_valid():
                insulin_food_form.save(user=request.user)
                return redirect('home')  # Refresh home page after save

    context = {
        'username': request.user.username if request.user.is_authenticated else None,
        'is_authenticated': request.user.is_authenticated,
        'bloodcheck_form': bloodcheck_form,
        'insulin_food_form': insulin_food_form,
        'form_type': form_type,  # Controls which form is displayed
    }
    return render(request, 'diabetes/home.html', context)


def insulin_detail(request, id):
    instance = get_object_or_404(InsulinInjection, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    jalali_date = date2jalali(instance.date).strftime("%Y/%m/%d")
    context = {
        'instance': instance,
        'type': 'InsulinInjection',
        'jalali_date': jalali_date,
    }
    return render(request, 'diabetes/instance_detail.html', context)


@login_required
def food_detail(request, id):
    instance = get_object_or_404(Food, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    jalali_date = date2jalali(instance.date).strftime("%Y/%m/%d")
    context = {
        'instance': instance,
        'type': 'Food',
        'jalali_date': jalali_date,
    }
    return render(request, 'diabetes/instance_detail.html', context)


@login_required
def bloodcheck_detail(request, id):
    instance = get_object_or_404(Bloodcheck, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    jalali_date = date2jalali(instance.date).strftime("%Y/%m/%d")
    context = {
        'instance': instance,
        'type': 'Bloodcheck',
        'jalali_date': jalali_date,
    }
    return render(request, 'diabetes/instance_detail.html', context)


@login_required
def insulin_edit(request, id):
    instance = get_object_or_404(InsulinInjection, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = InsulinFoodForm(user=request.user, data=request.POST)
        if form.is_valid():
            instance.insulin_type = form.cleaned_data['insulin_type']
            instance.insulin_dose = form.cleaned_data['insulin_dose']
            instance.time = form.cleaned_data['time']
            instance.date = form.cleaned_data['date']
            instance.injection_site = form.cleaned_data['injection_site']
            instance.save()
            return redirect('insulin_detail', id=id)
    else:
        form = InsulinFoodForm(user=request.user, initial={
            'insulin_type': instance.insulin_type,
            'insulin_dose': instance.insulin_dose,
            'time': instance.time.strftime('%H:%M'),
            'date': instance.date,
            'injection_site': instance.injection_site,
        })
    context = {'form': form, 'instance': instance, 'type': 'InsulinInjection'}
    return render(request, 'diabetes/instance_edit.html', context)


@login_required
def food_edit(request, id):
    instance = get_object_or_404(Food, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = InsulinFoodForm(user=request.user, data=request.POST)
        if form.is_valid():
            instance.food = form.cleaned_data['food']
            instance.carbs = form.cleaned_data['carbs']
            instance.time = form.cleaned_data['time']
            instance.date = form.cleaned_data['date']
            instance.save()
            return redirect('food_detail', id=id)
    else:
        form = InsulinFoodForm(user=request.user, initial={
            'food': instance.food,
            'carbs': instance.carbs,
            'time': instance.time.strftime('%H:%M'),
            'date': instance.date,
        })
    context = {'form': form, 'instance': instance, 'type': 'Food'}
    return render(request, 'diabetes/instance_edit.html', context)


@login_required
def bloodcheck_edit(request, id):
    instance = get_object_or_404(Bloodcheck, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        form = Bloodcheckform(request.POST, request.FILES)
        if form.is_valid():
            instance.bloodsugar = form.cleaned_data['bloodsugar']
            instance.time = form.cleaned_data['time']
            instance.date = form.cleaned_data['date']
            instance.event = form.cleaned_data['event']  # Add event
            instance.save()
            return redirect('bloodcheck_detail', id=id)
    else:
        form = Bloodcheckform(initial={
            'bloodsugar': instance.bloodsugar,
            'time': instance.time.strftime('%H:%M'),
            'date': instance.date,
            'event': instance.event,  # Add event
        })
    context = {'form': form, 'instance': instance, 'type': 'Bloodcheck'}
    return render(request, 'diabetes/instance_edit.html', context)


@login_required
def insulin_delete(request, id):
    instance = get_object_or_404(InsulinInjection, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        instance.delete()
        return redirect('insulin_food_list')
    context = {'instance': instance, 'type': 'InsulinInjection'}
    return render(request, 'diabetes/instance_delete.html', context)


@login_required
def food_delete(request, id):
    instance = get_object_or_404(Food, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        instance.delete()
        return redirect('insulin_food_list')
    context = {'instance': instance, 'type': 'Food'}
    return render(request, 'diabetes/instance_delete.html', context)


@login_required
def bloodcheck_delete(request, id):
    instance = get_object_or_404(Bloodcheck, id=id)
    if instance.user != request.user:
        return HttpResponseForbidden()
    if request.method == "POST":
        instance.delete()
        return redirect('bloodcheck_list')
    context = {'instance': instance, 'type': 'Bloodcheck'}
    return render(request, 'diabetes/instance_delete.html', context)
