import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect
from account.admin import UserCreationForm
from django.contrib.auth.models import Group
from projects.models import Case, ProjectDonation, ClosedDocs, ExtraDocs, ExtraImages
from datetime import datetime
from .forms import ProvisionalForm, MedicineForm, MedicalForm, EducationalForm, GeneralForm
from .filters import CaseFilter
from public.models import ImageSet, Photo
from blog.models import BlogPost
from account.decorators import allowed_roles
from events.models import Event, Volunteer
from datetime import datetime, timedelta
from spotlight.models import SpotlightImages, MediaSpotlight
from account.forms import ProfileForm
from projects.models import ProjectDonation
from account.models import AccountUser


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'user', 'subadmin'])
def profile(request):
    prof = request.user.userprofile_set.first()
    form = ProfileForm(instance=prof)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=prof)
        if form.is_valid():
            form.save()
        print(form.errors)
    context = {'form': form}
    return render(request, 'administration/profile.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def dashboard(request):
    this_month = datetime.now().date() - timedelta(days=30)
    recent_cases = Case.objects.filter(date_of_initiation__date__gte=this_month).order_by('priority', 'date_of_initiation')[:10]
    active_case_count = Case.objects.filter(status='Green').count()
    donations_this_month = ProjectDonation.objects.filter(date__date__gte=this_month)
    total_don_this_month = donations_this_month.aggregate(Sum('amount'))['amount__sum']

    context = {
        'recent_cases': recent_cases, 'active_count': active_case_count,
        'don_this_month': total_don_this_month
    }
    return render(request, 'administration/dashboard.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def donors(request):
    donations = ProjectDonation.objects.all().order_by('-date')
    total_donation = donations.aggregate(total=Sum('amount'))['total']
    donations_this_month = donations.filter(date__date__month=datetime.now().date().month).aggregate(total=Sum('amount'))['total']
    cards = [total_donation, donations_this_month]
    context = {'donations': donations, 'cards': cards}
    return render(request, 'administration/donations.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin'])
def users_list(request):
    users = AccountUser.objects.exclude(email='imranspeedcuber@gmail.com')
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        subadmin = AccountUser(
            email=email,
            password=password,
            username=email.split('@')[0],
            phone_number=phone,
            first_name=name,
        )
        subadmin.set_password(password)
        subadmin.save()
        grp = Group.objects.get(name='subadmin')
        subadmin.groups.add(grp)
    context = {'users': users}
    return render(request, 'administration/users.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin'])
def add_subadmin(request, pk):
    user = AccountUser.objects.get(id=pk)
    grp = Group.objects.get(name='subadmin')
    user.groups.add(grp)
    return redirect('a_users')


@login_required(login_url='login')
@allowed_roles(roles=['admin'])
def rem_subadmin(request, pk):
    user = AccountUser.objects.get(id=pk)
    grp = Group.objects.get(name='subadmin')
    user.groups.remove(grp)
    return redirect('a_users')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def all_cases(request):
    cases = Case.objects.all()
    case_filter = CaseFilter(request.GET, queryset=cases)
    cases = case_filter.qs

    sort = request.GET.get('sort', 'priority-d')
    f = sort.split('-')[0]
    o = sort.split('-')[1]

    order_by = '' if o == 'd' else '-'
    sorted_by = f'{order_by}{f}'

    closed_cases = cases.filter(status='Closed').order_by(sorted_by)
    active_cases = cases.filter(status='Green').order_by(sorted_by)
    rejected_cases = cases.filter(status='Red').order_by(sorted_by)
    pending_cases = cases.filter(status='Orange').order_by(sorted_by)
    p_case_count = pending_cases.count()
    a_case_count = active_cases.count()
    r_case_count = rejected_cases.count()

    context = {
        'pending_cases': pending_cases, 'p_count': p_case_count, 'a_count': a_case_count,
        'active_cases': active_cases, 'r_count': r_case_count, 'rejected_cases': rejected_cases,
        'closed_cases': closed_cases
    }

    return render(request, 'administration/all_cases.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def case_details(request, uuid):
    case = Case.objects.get(uuid=uuid)
    donations = ProjectDonation.objects.filter(case=case).order_by('-date')
    progress = (case.proper_total / case.requested_amount) * 100
    context = {'case': case, 'donations': donations, 'progress': progress}
    return render(request, 'administration/case_details.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def approve_case(request, uuid):
    case = Case.objects.get(uuid=uuid)
    if case.status != 'Green':
        case.status = 'Green'
        case.save()
    return redirect('a_case_details', uuid)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def close_case(request, uuid):
    case = Case.objects.get(uuid=uuid)
    if request.method == 'POST':
        c_docs = request.FILES.getlist('c_docs')

        case.status = 'Closed'
        case.save()

        for doc in c_docs:
            d = ClosedDocs.objects.create(doc=doc, case=case)
            d.save()

        messages.info(request, 'This Case Has Been Successfully Closed')
        return redirect('a_case_details', uuid)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def reject_case(request, uuid):
    case = Case.objects.get(uuid=uuid)
    if case.status != 'Red':
        case.status = 'Red'
        case.save()
    return redirect('a_case_details', uuid)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def add_case(request):
    profile = request.user.userprofile_set.all().first()
    formDict = {
        'General': GeneralForm, 'Educational': EducationalForm, 'Medical': MedicalForm, 'Medicine': MedicineForm,
        'Provisional': ProvisionalForm
    }
    t = request.GET.get('type', 'General')
    form = formDict[t]()

    if request.method == 'POST':
        form = formDict[t](request.POST, request.FILES)
        e_docs = request.FILES.getlist('e_docs')
        e_imgs = request.FILES.getlist('e_imgs')

        if form.is_valid():
            case = form.save(commit=False)
            case.type = str(t)
            case.created_by = profile
            case.save()

            for doc in e_docs:
                d = ExtraDocs.objects.create(doc=doc, case=case)
                d.save()

            for img in e_imgs:
                d = ExtraImages.objects.create(img=img, case=case)
                d.save()

            return redirect('a_case_details', case.uuid)

        messages.info(request, list(form.errors.values())[0])
    context = {'form': form, 'type': t}
    return render(request, 'administration/edit_case.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def edit_case(request, uuid):
    formDict = {
        'General': GeneralForm, 'Educational': EducationalForm, 'Medical': MedicalForm, 'Medicine': MedicineForm,
        'Provisional': ProvisionalForm
    }
    case = Case.objects.get(uuid=uuid)
    form = formDict[case.type](instance=case.get_proper_child())

    if request.method == 'POST':
        form = formDict[case.type](request.POST, request.FILES, instance=case.get_proper_child())
        e_docs = request.FILES.getlist('e_docs')
        e_imgs = request.FILES.getlist('e_imgs')

        if form.is_valid():
            c = form.save()
            c.has_finished

            for doc in e_docs:
                d = ExtraDocs.objects.create(doc=doc, case=c)
                d.save()

            for img in e_imgs:
                d = ExtraImages.objects.create(img=img, case=c)
                d.save()

            return redirect('a_case_details', case.uuid)
        messages.info(request, list(form.errors.values())[0])
    context = {'form': form, 'type': case.type, 'edit': True, 'case': case}
    return render(request, 'administration/edit_case.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin'])
def delete_case(request, uuid):
    case = Case.objects.get(uuid=uuid)
    case.delete()
    return redirect('a_cases')


def a_register(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            grp = Group.objects.get(name='admin')
            user.groups.add(grp)
            return redirect('a_login')
        messages.info(request, list(form.errors.values())[0])

    context = {'form': form}
    return render(request, 'account/register.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def media(request):
    spotlights = MediaSpotlight.objects.all().order_by('-date_published')
    context = {'spotlights': spotlights}
    return render(request, 'administration/media.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def gallery(request):
    gal_sets = ImageSet.objects.all().order_by('-date_created')

    if request.method == 'POST' and request.FILES['images']:
        images = request.FILES.getlist('images')
        title = request.POST.get('title')
        des = request.POST.get('description')

        img_set = ImageSet.objects.create(title=title, description=des)
        img_set.save()

        for img in images:
            p = Photo.objects.create(image=img, set=img_set)
            p.save()

    context = {'gal_sets': gal_sets}
    return render(request, 'administration/gallery.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def del_img_set(request, pk):
    img_set = ImageSet.objects.get(id=pk)
    for img in img_set.photo_set.all():
        img.delete()
    img_set.delete()
    return redirect('a_gallery')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def del_img(request, pk):
    img = Photo.objects.get(id=pk)
    img.delete()
    return redirect('a_gallery')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def add_new_images(request, pk):
    img_set = ImageSet.objects.get(id=pk)

    if request.method == 'POST' and request.FILES['images']:
        images = request.FILES.getlist('images')

        for img in images:
            p = Photo.objects.create(image=img, set=img_set)
            p.save()

        return redirect('a_gallery')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def blog(request):
    blogs = BlogPost.objects.all().order_by('-posted_on')
    context = {'blogs': blogs}
    return render(request, 'administration/blog.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def events(request):
    today = datetime.now().date()
    upcoming_events = Event.objects.filter(start_date__gte=today).order_by('start_date')
    context = {'events': upcoming_events}
    return render(request, 'administration/events.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def volunteer(request):
    applications = Volunteer.objects.all().order_by('-application_date')
    context = {'applications': applications}
    return render(request, 'administration/volunteer.html', context)