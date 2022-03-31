from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .admin import UserCreationForm
from django.contrib.auth.models import Group
from .forms import ProfileForm
from account.forms import ProfileForm


def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            if user.groups.all().first() is not None:
                if user.groups.all().first().name == 'admin':
                    return redirect('a_dashboard')
                else:
                    if user.userprofile_set.all().first() is not None:
                        return redirect('all_cases')
                    else:
                        return redirect('complete_profile')
        else:
            messages.info(request, 'Email or password is incorrect')
    return render(request, 'account/login.html')


def logout_user(request):
    logout(request)
    return redirect('index')


def register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            grp = Group.objects.get(name='user')
            user.groups.add(grp)
            return redirect('login')

        messages.info(request, list(form.errors.values())[0])

    context = {'form': form}
    return render(request, 'account/register.html', context)


@login_required(login_url='login')
def complete_profile(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            prof = form.save(commit=False)
            prof.user = request.user
            prof.save()
            return redirect('all_cases')
    context = {'form': form}
    return render(request, 'account/complete_profile.html', context)


def change_password(request):
    return render(request, 'account/change_pw.html')


def profile(request):
    prof = request.user.userprofile_set.first()
    form = ProfileForm(instance=prof)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=prof)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'account/profile.html', context)


def new_pw(request):
    return render(request, 'account/confirm_new_pw.html')
