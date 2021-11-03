from django.shortcuts import render, redirect
from .models import Source, Income
from django.core.paginator import Paginator
from userpreferences.models import UserPreference
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
# Create your views here.


def search_income(request):
    if request.method == 'POST':
        search_string = json.loads(request.body).get('searchText')

        income = Income.objects.filter(
            amount__startswith=search_string, owner=request.user) | Income.objects.filter(
                date__startswith=search_string, owner=request.user) | Income.objects.filter(
                    description__icontains=search_string, owner=request.user) | Income.objects.filter(
                        source__icontains=search_string, owner=request.user)

        data = income.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='authentication/login')
def index(request):
    income = Income.objects.filter(owner=request.user)
    paginator = Paginator(income, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        currency = 'INR'
    context = {
        'income': income,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'income/index.html', context)


@login_required(login_url='authentication/login')
def add_income(request):
    sources = Source.objects.all()
    context = {'sources': sources, 'values': request.POST}
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/add_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/add_income.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/add_income.html', context)

        Income.objects.create(amount=amount, date=date, source=source,
                              description=description, owner=request.user)
        messages.success(request, 'Income saved successfully')
        return redirect('income')
    return render(request, 'income/add_income.html', context)


def income_edit(request, id):
    income = Income.objects.get(pk=id)
    sources = Source.objects.all()
    context = {
        'income': income,
        'sources': sources,
        'values': income
    }

    if request.method == 'GET':
        return render(request, 'income/edit_income.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        source = request.POST['source']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'income/edit_income.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'income/edit_income.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'income/edit_income.html', context)

        income.amount = amount
        income.date = date
        income.source = source
        income.description = description
        income.owner = request.user
        income.save()
        messages.success(request, 'Income Updated successfully')
        return redirect('income')
    return render(request, 'income/edit_income.html', context)


def income_delete(request, id):
    income = Income.objects.get(pk=id)
    income.delete()
    messages.success(request, 'Income Deleted successfully')

    return redirect('income')
