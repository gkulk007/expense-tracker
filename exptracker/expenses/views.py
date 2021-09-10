from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages
# Create your views here.


@login_required(login_url='authentication/login')
def index(request):
    expenses = Expense.objects.filter(owner=request.user)
    context = {
        'expenses': expenses
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
