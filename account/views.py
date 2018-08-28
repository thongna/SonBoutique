from django.shortcuts import render
from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from account.check_user import is_admin, is_customer, is_staff, is_staff_view

# Create your views here.
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            user = None
            try:
                user = User.objects.get(username=username)
            except:
                pass
            if user:
                raise user_form.ValidationError("Username is already registered!")
            else:
                # Create a new user object but avoid saving it yet
                new_user = user_form.save(commit=False)
                # Set the chosen password
                new_user.set_password(user_form.cleaned_data['password'])
                # Save the User object
                new_user.save()
                Profile.objects.create(user=new_user)
                return render(request, 'registration/register_done.html',
                              {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form})

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Thông tin của bạn đã được cập nhật thành công.')
        else:
            messages.error(request, 'Lỗi khi cập nhật thông tin của bạn. Vui lòng kiểm tra lại.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    usergroup = request.user.groups.values_list('name', flat=True).first()
    if usergroup:
        return render(request, 'registration/editprofile.html',
                  {'user_form': user_form,
                   'profile_form': profile_form})
    else:
        return render(request, 'registration/editprofile_for_customer.html',
                      {'user_form': user_form,
                       'profile_form': profile_form})


def loggedin_view(request):
    usergroup = None
    try:
        if request.user:
            usergroup = request.user.groups.values_list('name', flat=True).first()
        if usergroup:
            if usergroup == "Administrator":
                return HttpResponseRedirect('/admin/')
            elif usergroup == "staff" or usergroup == "staff_view":
                return HttpResponseRedirect("/statisticadmin/dashboard")
            elif usergroup == "customer":
                return HttpResponseRedirect("/admin")
        else:
            return HttpResponseRedirect("/")
    except Exception as e:
        print(e)