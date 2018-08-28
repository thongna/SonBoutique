from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from account.check_user import is_admin, is_customer, is_staff, is_staff_view
from orders.models import OrderItem, Order
from finance.models import Expenses
from shop.models import Product
from django.db.models import Sum, Q
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count
from django.utils.timezone import datetime
from django.contrib.auth.decorators import permission_required

@user_passes_test(is_staff)
@login_required
def home(request):
    order_items = OrderItem.objects.all()
    products = Product.objects.all()
    orders = Order.objects.all()
    # total orderd items
    total_order_items = order_items.aggregate(total_order=Sum('quantity'))['total_order']
    # total saled items
    total_saled_items = order_items.filter(order__paid=True).aggregate(total_saled=Sum('quantity'))['total_saled']
    # total income of saled items
    income_amounts = "{:,}".format(orders.filter(paid=True).aggregate(income_amounts=Sum('total_price'))['income_amounts'])
    # total stock
    total_stock = products.aggregate(total_stock=Sum('stock'))['total_stock']

    # data for highchart
    select_data = {"create": """strftime('%%d-%%m-%%Y', created)"""}
    # income
    dataset = Order.objects.filter(paid=True).extra(select=select_data).values('create').annotate(
        income=Sum('total_price')).order_by('-create')[:10]
    # total orders by day
    total_order_by_day = Order.objects.filter(paid=True).extra(select=select_data).values('create').annotate(
        total_order=Count('id')).order_by('-create')[:10]
    # total items by day
    total_items_by_day = OrderItem.objects.filter(order__paid=True).extra(select=select_data).values('create').annotate(
        total_items=Sum('quantity')).order_by('-create')[:10]
    # top 5 of the saled items
    total_saled_items_by_type = products.extra(select={"names":"names"}).values('name').annotate(quantity=Sum('saled')).order_by('-quantity')[:5]
    # top 5 of the items in stock
    items_in_stock_by_type = products.extra(select={"names":"names"}).values('name').annotate(quantity=Sum('stock')).order_by('-quantity')[:5]
    context = {
        'total_order_items': total_order_items,
        'total_saled_items': total_saled_items,
        'income_amounts': income_amounts,
        'total_stock': total_stock,
        'orders': orders[:10],
        'dataset': dataset,
        'total_order_by_day': total_order_by_day,
        'total_items_by_day': total_items_by_day,
        'total_saled_items_by_type': total_saled_items_by_type,
        'items_in_stock_by_type': items_in_stock_by_type,

    }
    return render(request,
                  'statisticadmin/dashboard/dashboard.html',
                  context)

# Order List
@user_passes_test(is_staff_view)
@login_required
def order(request, day=None, month=None, paid=None):
    today = datetime.now()
    order_list = Order.objects.all().order_by('paid', '-created')
    title = ''
    amount= ''
    search = request.GET.get('q')
    filter = request.POST.get('pay')
    if filter:
        order_list = order_list.filter(paid=0)
    if search:
        order_list=order_list.filter(phone_number=search)
        amount = 'TỔNG TIỀN ĐÃ MUA {} VND'.format(order_list.aggregate(amount=Sum('total_price'))['amount'])
        title = 'THEO SĐT {}'.format(search)
    else:
        if day:
            order_list = order_list.filter(created__day=day.split('-')[0], created__month=day.split('-')[1], created__year=day.split('-')[2])
            title = 'NGÀY {}'.format(day)
        if month:
            order_list = order_list.filter(created__month=month.split("-")[0], created__year=month.split('-')[1])
            title = 'THÁNG ' + str(month)
        if paid == 1:
            order_list = order_list.filter(paid=True)
        elif paid == 0:
            order_list = order_list.filter(paid=False)
    paginator = Paginator(order_list, 10)  # 10 orders in each page
    page = request.GET.get('page')
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        orders = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        orders = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'orders': orders,
        'title': title,
        'amount': amount
    }
    return render(request, 'statisticadmin/order/order.html', context)

# Change order paid is True
@user_passes_test(is_staff_view)
@login_required
@require_POST
def order_paid(request):
    order_id = request.POST.get('id')
    if order_id:
        try:
            order = Order.objects.get(id=order_id)
            order.paid = True
            order.save()
            order_items = OrderItem.objects.filter(order=order)
            for order_item in order_items:
                product = Product.objects.get(id=order_item.product.id)
                product.stock -= order_item.quantity
                product.saled += order_item.quantity
                product.save()
            return JsonResponse({'status': 'ok', 'order_id': order_id})
        except:
            pass
    return JsonResponse({'status': 'ko', 'order_id': order_id})

# Stock List
@user_passes_test(is_staff_view)
@login_required
def stock_list(request):
    product_list = Product.objects.filter(available=True, stock__gt=0)
    search = request.GET.get('q')
    if search:
        product_list = product_list.filter(Q(product_code__contains=search) | Q(name__contains=search.upper()) | Q(name__contains=search.lower()))
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        products = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        products = paginator.page(paginator.num_pages)
    context = {
        'products': products,
    }
    return render(request, 'statisticadmin/dashboard/warehouse.html', context)

# Revenue List
@user_passes_test(is_staff_view)
@login_required
def revenue(request):
    search = request.GET.get('d')
    today = datetime.now().strftime('%d-%m-%Y')
    orders = Order.objects.filter(paid=True)
    try:
        # income
        income_total = "{:,}".format(orders.aggregate(income_amounts=Sum('total_price'))['income_amounts'])
        income_today = orders.filter(created__day=today.split('-')[0], created__month=today.split('-')[1], created__year=today.split('-')[2]).aggregate(income_amounts=Sum('total_price'))[
            'income_amounts']
        if income_today is None:
            income_today = 0
        income_month = orders.filter(created__month=today.split('-')[1], created__year=today.split('-')[2]).aggregate(income_amounts=Sum('total_price'))[
            'income_amounts']
        if income_month is None:
            income_today = 0      # order
        order_total = orders.count()
        order_today = orders.filter(created__day=today.split('-')[0], created__month=today.split('-')[1], created__year=today.split('-')[2]).count()
        order_month = orders.filter(created__month=today.split('-')[1], created__year=today.split('-')[2]).count()
        # compare
        income_yesterday = \
        orders.filter(created__day=(int(today.split('-')[0]) - 1), created__month=today.split('-')[1], created__year=today.split('-')[2]).aggregate(income_amounts=Sum('total_price'))[
            'income_amounts']
        income_last_month = \
        orders.filter(created__month=(int(today.split('-')[1]) - 1), created__year=today.split('-')[2]).aggregate(income_amounts=Sum('total_price'))[
            'income_amounts']
        if income_yesterday and income_yesterday != 0:
            income_day_rate = (income_today - income_yesterday) / income_yesterday * 100
        else:
            income_day_rate = 100

        if income_last_month and income_last_month != 0:
            income_month_rate = (income_month - income_last_month) / income_last_month * 100
        else:
            income_month_rate = 100

        income_today = "{:,}".format(income_today)
        income_month = "{:,}".format(income_month)

        # data for highchart
        select_data_by_day = {"create": """strftime('%%d-%%m-%%Y', created)"""}
        select_data_by_month = {"create": """strftime('%%m-%%Y', created)"""}
        # income

        income_month_dataset = orders.extra(select=select_data_by_month).values('create').annotate(income=Sum('total_price')).order_by('-create')[:10]

        income_day_dataset_all = orders.extra(select=select_data_by_day).values('create').annotate(
            income=Sum('total_price')).order_by('-create')
        if search:
            income_day_dataset_all = [income for income in income_day_dataset_all if income['create'] == search]
    except:
        pass


    paginator = Paginator(income_day_dataset_all, 10)  # 10 orders in each page
    page = request.GET.get('page')
    try:
        income_day_dataset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        income_day_dataset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        income_day_dataset = paginator.page(paginator.num_pages)

    context = {
        'today':today,
        'month': today.split('-')[1] + "-" + today.split('-')[2],
        'income_total': income_total,
        'income_today': income_today,
        'income_month': income_month,
        'order_total': order_total,
        'order_today': order_today,
        'order_month': order_month,
        'income_day_rate': income_day_rate,
        'income_month_rate': income_month_rate,
        'income_day_dataset': income_day_dataset,
        'income_month_dataset': income_month_dataset,
        'page': page,

    }
    return render(request, 'statisticadmin/dashboard/revenue.html', context)

# Expenses list
@user_passes_test(is_staff_view)
@login_required
def expenses(request):
    expense_list = Expenses.objects.all()
    title = ''
    expense_month = 0
    expense_last_month = 0
    expense_month_dataset_all =[]
    m = None
    expense_month_rate = None
    search = request.GET.get('m')
    try:
        # expenses month
        m = datetime.now().month
        y = datetime.now().year
        expense_month = expense_list.filter(month__month=m, month__year=y).aggregate(cost=Sum('amount'))['cost']
        expense_last_month = expense_list.filter(month__month=(m-1), month__year=y).aggregate(cost=Sum('amount'))['cost']
        if expense_last_month is None:
            expense_last_month = 0
        if expense_last_month!=0:
            expense_month_rate = (expense_month - expense_last_month)/expense_last_month*100
        else:
            expense_month_rate = 100
     
        # high chart
        select_data_by_month = {"create": """strftime('%%m-%%Y', month)"""}
        expense_month_dataset_all = expense_list.extra(select=select_data_by_month).values('create').annotate(expense=Sum('amount')).order_by('-create')
    except Exception as e:
        print(e)
        pass
    expense_month = "{:,}".format(expense_month)
    expense_last_month = "{:,}".format(expense_last_month)

    if search:
        expense_month_dataset_all = [expense for expense in expense_month_dataset_all if expense['create'] == search]
        title = 'THÁNG {}'.format(search)

    paginator = Paginator(expense_month_dataset_all, 10)  # 10 orders in each page
    page = request.GET.get('page')
    try:
        expense_month_dataset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        expense_month_dataset = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        expense_month_dataset = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'expenses': expenses,
        'title': title,
        'expense_month': expense_month,
        'expense_last_month': expense_last_month,
        'expense_month_dataset': expense_month_dataset,
        'month': str(m) + "-" + str(y),
        'last_month': str(m-1) + "-" + str(y),
        'expense_month_rate': expense_month_rate
    }
    return render(request, "statisticadmin/dashboard/expenses.html", context)

def expense_list(request, month=None):
    expense_list = Expenses.objects.all()
    title = ''
    m = month
    search = request.GET.get('q')
    if search:
        expense_list = expense_list.filter(Q(name__name__contains=search) | Q(create_by__username=search))
        title = 'TÌM KIẾM THEO "{}"'.format(search.upper())
    if month:
        expense_list = expense_list.filter(month__month=month.split('-')[0], month__year=month.split('-')[1])
        title = 'THÁNG ' + str(month)

    paginator = Paginator(expense_list, 10)  # 10 orders in each page
    page = request.GET.get('page')
    try:
        expenses = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        expenses = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        expenses = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'expenses': expenses,
        'title': title,
    }
    return render(request, "statisticadmin/dashboard/expense-list.html", context)

def profit(request):
    expense_list = Expenses.objects.all()
    order_items = OrderItem.objects.filter(order__paid=True)
    orders = Order.objects.filter(paid=True)
    title = ''
    expense_month = None
    search = request.GET.get('m')
    m = datetime.now().month
    y = datetime.now().year
    qt = None
    q = []
    quarter_list = ([1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12])

    for quarter in quarter_list:
        if m in quarter:
            q = quarter
            qt = quarter_list.index(quarter) + 1

    # Expenses
    expense_month = expense_list.filter(month__month=m, month__year=y).aggregate(cost=Sum('amount'))['cost']
    expense_last_month = expense_list.filter(month__month=(m-1), month__year=y).aggregate(cost=Sum('amount'))['cost']
    expense_quarter = expense_list.filter(month__month__in=q, month__year=y).aggregate(cost=Sum('amount'))['cost']
    expense_year = expense_list.filter(month__year=y).aggregate(cost=Sum('amount'))['cost']

    if expense_month is None:
        expense_month = 0
    if expense_last_month is None:
        expense_last_month = 0
    if expense_quarter is None:
        expense_quarter = 0
    if expense_year is None:
        expense_year = 0

    # Revenue
    income_month = orders.filter(paid=True, created__month=m, created__year=y).aggregate(income_amounts=Sum('total_price'))['income_amounts']
    income_last_month = orders.filter(paid=True, created__month=(m-1), created__year=y).aggregate(income_amounts=Sum('total_price'))[
        'income_amounts']
    income_quarter = orders.filter(paid=True, created__month__in=q, created__year=y).aggregate(income_amounts=Sum('total_price'))[
        'income_amounts']
    income_year = orders.filter(paid=True, created__year=y).aggregate(income_amounts=Sum('total_price'))[
        'income_amounts']

    if income_month is None:
        income_month = 0
    if income_last_month is None:
        income_last_month = 0
    if income_quarter is None:
        income_quarter = 0
    if income_year is None:
        income_year = 0

    # total saled items
    total_saled_items_in_month = order_items.filter(order__created__month=m, order__created__year=y).aggregate(total_saled=Sum('quantity'))['total_saled']
    total_saled_items_in_quarter = order_items.filter(order__created__month__in=q, order__created__year=y).aggregate(total_saled=Sum('quantity'))['total_saled']
    total_saled_items_in_year = order_items.filter(order__created__year=y).aggregate(total_saled=Sum('quantity'))['total_saled']

    # profit
    profit_month = income_month - expense_month
    profit_last_month = income_last_month - expense_last_month
    if profit_last_month != 0:
        profit_month_rate = (profit_month - profit_last_month)/profit_last_month*100
    else:
        profit_month_rate = 100

    profit_month = "{:,}".format(profit_month)
    profit_quarter = "{:,}".format(income_quarter - expense_quarter)
    profit_year = "{:,}".format(income_year - expense_year)

    select_data_by_month_for_income = {"create": """strftime('%%m-%%Y', created)"""}
    select_data_by_month_for_expense = {"create": """strftime('%%m-%%Y', month)"""}
    income_month_dataset = Order.objects.filter(paid=True).extra(select=select_data_by_month_for_income).values('create').annotate(income=Sum('total_price')).order_by('-create')
    expense_month_dataset = expense_list.extra(select=select_data_by_month_for_expense).values('create').annotate(expense=Sum('amount')).order_by('-create')

    finance_list = []
    for im in income_month_dataset:
        added = False # to check if find expense in month
        for em in expense_month_dataset:
            if em['create'] == im['create']:
                finance_list.append({'create': im['create'], 'income': im['income'], 'expense': em['expense'], 'profit': (im['income'] - em['expense'])})
                added = True
                break
        if added is False:
            finance_list.append({'create': im['create'], 'income': im['income'], 'expense': 0, 'profit': im['income']})

    for em in expense_month_dataset:
        is_have = False # to check whether finance has expense of this month
        for f in finance_list:
            if f['create'] == em['create']:
                is_have = True
                break
        if is_have is False:
            finance_list.append({'create': em['create'], 'income': 0, 'expense': em['expense'], 'profit': -em['expense']})

    if search:
        finance_list = [finance for finance in finance_list if finance['create'] == search]
        title = 'THÁNG "{}"'.format(search.upper())

    paginator = Paginator(finance_list, 10)  # 10 orders in each page
    page = request.GET.get('page')
    try:
        finance = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        finance = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        finance = paginator.page(paginator.num_pages)

    context = {
        'profit_month': profit_month,
        'profit_quarter': profit_quarter,
        'profit_year': profit_year,
        'profit_month_rate': profit_month_rate,
        'total_saled_items_in_month': total_saled_items_in_month,
        'total_saled_items_in_quarter': total_saled_items_in_quarter,
        'total_saled_items_in_year': total_saled_items_in_year,
        'finance': finance,
        'page': page,
        'title': title,
        'm': m,
        'qt': qt,
        'y': y,

    }
    return render(request, 'statisticadmin/dashboard/profit.html', context)
