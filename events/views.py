from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import EventForm, VolunteerForm
from .models import Event, Volunteer
from datetime import datetime
from account.decorators import allowed_roles


def events(request):
    today = datetime.now().date()
    upcoming = Event.objects.filter(start_date__gte=today)
    context = {'upcoming': upcoming}
    return render(request, 'events/index.html', context)


def event_details(request, pk):
    event = Event.objects.get(id=pk)
    others = Event.objects.exclude(id=pk).order_by('start_date')
    context = {'event': event, 'others': others}
    return render(request, 'events/details.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def add_event(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('a_events')
    context = {'form': form}
    return render(request, 'events/add_event.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def edit_event(request, pk):
    event = Event.objects.get(id=pk)
    form = EventForm(instance=event)
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('a_events')
        print(form.errors)
    context = {'form': form, 'edit': True, 'event': event}
    return render(request, 'events/add_event.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def del_event(request, pk):
    event = Event.pbjects.get(id=pk)
    event.delete()
    return redirect('a_events')


def volunteer(request):
    form = VolunteerForm
    if request.method == 'POST':
        form = VolunteerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('v_successful')
    context = {'form': form}
    return render(request, 'events/volunteer.html', context)


def volunteer_successful(request):
    return render(request, 'events/submitted.html')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def volunteer_accept(request, pk):
    application = Volunteer.objects.get(id=pk)
    application.status = 'Accepted'
    application.save()
    return redirect('a_volunteer')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def volunteer_reject(request, pk):
    application = Volunteer.objects.get(id=pk)
    application.status = 'Rejected'
    application.save()
    return redirect('a_volunteer')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def vol_del(request, pk):
    application = Volunteer.objects.get(id=pk)
    application.delete()
    return redirect('a_volunteer')