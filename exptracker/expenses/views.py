from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from userpreferences.models import UserPreference
# Create your views here.


def search_expenses(request):
    if request.method == 'POST':
        search_string = json.loads(request.body).get('searchText')

        expenses = Expense.objects.filter(
            amount__startswith=search_string, owner=request.user) | Expense.objects.filter(
                date__startswith=search_string, owner=request.user) | Expense.objects.filter(
                    description__icontains=search_string, owner=request.user) | Expense.objects.filter(
                        category__icontains=search_string, owner=request.user)

        data = expenses.values()

        return JsonResponse(list(data), safe=False)


@login_required(login_url='authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 2)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    currency = UserPreference.objects.get(user=request.user).currency
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency,
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {'categories': categories, 'values': request.POST}
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expenses.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/add_expenses.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/add_expenses.html', context)

        Expense.objects.create(amount=amount, date=date, category=category,
                               description=description, owner=request.user)
        messages.success(request, 'Expense saved successfully')
        return redirect('expenses')
    return render(request, 'expenses/add_expenses.html', context)


def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'categories': categories,
        'values': expense
    }

    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']
        description = request.POST['description']
        date = request.POST['date']
        category = request.POST['category']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        if not description:
            messages.error(request, 'Description is required')
            return render(request, 'expenses/edit-expense.html', context)

        if not date:
            messages.error(request, 'Date is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.amount = amount
        expense.date = date
        expense.category = category
        expense.description = description
        expense.owner = request.user
        expense.save()
        messages.success(request, 'Expense Updated successfully')
        return redirect('expenses')
    return render(request, 'expenses/edit-expense.html', context)


def expense_delete(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense Deleted successfully')

    return redirect('expenses')
