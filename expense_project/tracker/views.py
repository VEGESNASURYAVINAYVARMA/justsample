from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ExpenseForm
from .models import Expense

from django.db.models.functions import TruncMonth
from django.db.models import Sum


def home(request):
    return render(request, 'home.html')


def register(request):
    from .forms import RegisterForm

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # go to login page
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


from datetime import datetime
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Expense
from django.db.models.functions import TruncMonth
from django.db.models import Sum

import json

@login_required
def dashboard(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        amount = request.POST.get('amount')
        date = request.POST.get('date')

        is_long_term = request.POST.get('is_long_term') == 'on'
        end_date = request.POST.get('end_date') or None
        interest_rate = request.POST.get('interest_rate') or None

        Expense.objects.create(
            user=request.user,
            name=name,
            amount=float(amount),
            date=date,
            is_long_term=is_long_term,
            end_date=end_date,
            interest_rate=interest_rate
        )

        return redirect('dashboard')

    expenses = Expense.objects.filter(user=request.user).order_by('-date')

    # MONTHLY CALCULATION
    from django.db.models.functions import TruncMonth
    from django.db.models import Sum

    monthly = (
        Expense.objects.filter(user=request.user)
        .annotate(month=TruncMonth('date'))
        .values('month')
        .annotate(total=Sum('amount'))
        .order_by('month')
    )

    labels = []
    data = []

    for m in monthly:
        labels.append(m['month'].strftime('%b %Y'))
        data.append(float(m['total']))

    return render(request, 'dashboard.html', {
        'expenses': expenses,
        'labels': json.dumps(labels),
        'data': json.dumps(data),
    })