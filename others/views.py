from django.shortcuts import render
from .models import Contact, Question, QuestionType, Messages
from shop.models import Comment
from .forms import MessagesForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required, user_passes_test
from account.check_user import is_admin, is_customer, is_staff, is_staff_view
from django.http import JsonResponse
from django.db.models import Q

# Create your views here.

def contact(request):
    son_boutique_contact = Contact.objects.get(name="Son Boutique")

    if request.method == 'POST':
        message_form = MessagesForm(data=request.POST)
        if message_form.is_valid():
            message_form.save()
        message_form = MessagesForm()
    else:
        message_form = MessagesForm()

    context = {
        'son_boutique_contact': son_boutique_contact,
        'message_form': message_form,
    }
    return render(request, 'others/other/contact.html', context)

@login_required
@user_passes_test(is_staff_view)
def review_list(request):
    comment_list = Comment.objects.all()
    title = ''
    search = request.GET.get('q')
    if search:
        comment_list = comment_list.filter(body__contains=search)
        title = 'THEO TỪ KHÓA "{}"'.format(search)
    paginator = Paginator(comment_list, 10)  # 10 orders in each page
    page = request.GET.get('page')
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        comments = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        comments = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'comments': comments,
        'title': title,
    }
    return render(request, 'others/other/review.html', context)


# Change order paid is True
@login_required
@user_passes_test(is_staff_view)
@require_POST
def review_active(request):
    comment_id = request.POST.get('id')
    comment_status = request.POST.get('active')
    if comment_id and comment_status:
        try:
            comment = Comment.objects.get(id=comment_id)
            if comment_status == '1':
                comment.active = True
            elif comment_status == '0':
                comment.active = False
            comment.save()
            return JsonResponse({'status': 'ok', 'comment_id': comment_id, 'comment_status': comment_status})
        except:
            pass
    return JsonResponse({'status': 'ko', 'comment_id': comment_id, 'comment_status': comment_status})

# Page Not Found
def error_404_view(request):
    return render(request,'others/other/404_page.html')

def faq(request):
    question_types = QuestionType.objects.all()
    faq_list = Question.objects.all()
    return render(request, 'others/other/FAQ.html', {'faq_list': faq_list,
                                                     'question_types': question_types})

def aboutus(request):
    return render(request, 'others/other/aboutus.html')

@login_required
@user_passes_test(is_staff_view)
def message_list(request):
    message_list = Messages.objects.all().order_by('readed')
    title = ''
    search = request.GET.get('q')
    if search:
        message_list = message_list.filter(Q(body__contains=search) | Q(title__contains=search) | Q(name__contains=search) | Q(phone_number=search))
        title = 'THEO TỪ KHÓA "{}"'.format(search)
    paginator = Paginator(message_list, 10)  # 10 orders in each page
    page = request.GET.get('page')
    try:
        messages = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        messages = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        messages = paginator.page(paginator.num_pages)
    context = {
        'page': page,
        'messages': messages,
        'title': title,
    }
    return render(request, 'others/other/messages.html', context)

# Change order paid is True
@user_passes_test(is_staff_view)
@login_required
@require_POST
def message_readed(request):
    message_id = request.POST.get('id')
    if message_id:
        try:
            message = Messages.objects.get(id=message_id)
            message.readed = True
            message.save()
            return JsonResponse({'status': 'ok', 'message_id': message_id})
        except:
            pass
    return JsonResponse({'status': 'ko', 'message_id': message_id})