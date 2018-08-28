from django.shortcuts import render
from .forms import ExpenseForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from account.check_user import is_admin, is_customer, is_staff, is_staff_view

# Create your views here.
@user_passes_test(is_staff)
@login_required
def import_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            user = User.objects.get(username=request.user.username)
            expense.create_by = user
            expense.save()
            messages.success(request, 'Bạn đã nhập chi phí {} tháng {} thành công.'.format(expense.name, expense.month))
        form = ExpenseForm()
        return render(request, 'finance/import_expenses.html', {'form': form})
    else:
        form = ExpenseForm()
    context = {
        'form': form,
    }
    return render(request, 'finance/import_expenses.html', context)