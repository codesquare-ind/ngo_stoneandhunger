import hashlib
import tempfile
import uuid
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string, get_template
from django.views.decorators.csrf import csrf_exempt
from paywix.payu import Payu
from weasyprint import HTML, CSS
from xhtml2pdf import pisa

from .models import Case, ProjectDonation, ExtraDocs, ExtraImages
from django.conf import settings
from account.models import UserProfile, AccountUser
from administration.filters import CaseFilter
from administration.forms import GeneralForm, MedicalForm, MedicineForm, EducationalForm, ProvisionalForm
from account.decorators import allowed_roles
from django.db.models import Q
from .utils import send_email_invoice
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


@login_required(login_url='login')
@allowed_roles(roles=['user'])
def dashboard(request):
    profile = request.user.userprofile_set.all().first()

    donations = ProjectDonation.objects.filter(donor=request.user).order_by('-date')
    cases = Case.objects.filter(created_by=profile, status='Green').order_by('-date_of_initiation')

    total_donation = donations.aggregate(total=Sum('amount'))['total']
    total_received = cases.aggregate(total=Sum('total_collected'))['total']

    context = {'donations': donations, 'cases': cases, 'total_don': total_donation, 'total_rec': total_received}
    return render(request, 'projects/dashboard.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['user'])
def my_cases(request):
    profile = request.user.userprofile_set.first()
    cases = Case.objects.filter(created_by=profile).order_by('-date_of_initiation')

    approved = cases.filter(status='Green')
    pending = cases.filter(status='Orange')
    rejected = cases.filter(status='Red')

    total_received = cases.aggregate(total=Sum('total_collected'))['total']

    context = {'cases': cases, 'approved': approved, 'received': total_received, 'pending': pending, 'rejected': rejected}
    return render(request, 'projects/cases.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['user'])
def my_donations(request):
    this_month = datetime.now().month
    all_donations = ProjectDonation.objects.filter(donor=request.user).order_by('-date')

    total_donation = all_donations.aggregate(total=Sum('amount'))['total']
    month_donation = all_donations.filter(date__date__month=this_month).aggregate(total=Sum('amount'))['total']

    context = {'all_d': all_donations, 'total': total_donation, 'month': month_donation}
    return render(request, 'projects/donations.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['user'])
def create_new_case(request):
    profile = request.user.userprofile_set.all().first()
    formDict = {
        'General': GeneralForm, 'Educational': EducationalForm, 'Medical': MedicalForm, 'Medicine': MedicineForm,
        'Provisional': ProvisionalForm
    }
    t = request.GET.get('type', 'General')
    form = formDict[t]()

    if request.method == 'POST':
        request.POST = request.POST.copy()
        request.POST['status'] = 'Orange'
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

            return redirect('case_details', case.uuid)
        print(form.errors)
    context = {'form': form, 'type': t}
    return render(request, 'projects/post_case.html', context)


def all_cases(request):
    top_cases = Case.objects.filter(Q(status='Green') | Q(status='Closed')).order_by('priority').order_by('-date_of_initiation')
    c_filter = CaseFilter(request.GET, queryset=top_cases)
    top_cases = c_filter.qs

    context = {
        'all_cases': top_cases
    }
    return render(request, 'projects/all_cases.html', context)


def case_details(request, uuid):
    case = Case.objects.get(uuid=uuid)
    context = {'case': case}
    return render(request, 'projects/case_details.html', context)


# payment gateway

payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create payu instance
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)


@csrf_exempt
def checkout(request, id=' '):
    if request.method == 'POST':
        amount = request.POST.get('amount')
        case_id = str(id)

        category = request.POST.get('type')

        if request.user.is_authenticated:
            profile = UserProfile.objects.filter(user=request.user).first()
            firstname = request.user.first_name
            lastname = request.user.last_name
            phone = request.user.phone_number
            email = request.user.email
            address = profile.address
            city = profile.city
            state = profile.state
            country = profile.country
            gender = profile.gender
            pan = request.POST.get('pan')
        else:
            firstname = request.POST.get('first_name')
            lastname = request.POST.get('last_name')
            phone = request.POST.get('phone')
            email = request.POST.get('email')
            address = request.POST.get('address')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')
            gender = request.POST.get('gender')
            pan = request.POST.get('pan')

        data = {
            'amount': f'{amount}', 'firstname': f'{firstname}',
            'email': f'{email}', 'phone': f'{phone}', 'productinfo': f'donation-{category}-{case_id}',
            'lastname': f'{lastname}', 'address1': f'{address}',
            'address2': '', 'city': f'{city}', 'state': f'{state}', 'country': f'{country}',
            'zipcode': 'tes', 'udf1': '', 'udf2': f'{gender}', 'udf3': f'{pan}', 'udf4': '', 'udf5': '',
        }
        # Make sure the transaction ID is unique
        prefix = 'tmk'
        new_id = str(uuid.uuid4())
        hash_object = hashlib.sha256(new_id.encode())
        txnid = f'{prefix} {hash_object.hexdigest()[0:20]}'

        data.update({"txnid": txnid})
        payu_data = payu.transaction(**data)

        context = {'posted': payu_data}
        return render(request, 'projects/checkout.html', context)


@csrf_exempt
def success(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)

    firstname = response['return_data'].get('firstname')
    lastname = response['return_data'].get('lastname')
    email = response['return_data'].get('email')
    phone = response['return_data'].get('phone')
    address = response['return_data'].get('address1')
    state = response['return_data'].get('state')
    country = response['return_data'].get('country')
    city = response['return_data'].get('city')
    gender = response['return_data'].get('udf2')
    pan = response['return_data'].get('udf3')
    category = response['return_data'].get('productinfo').split('-')[1]

    trans_id = response['return_data'].get('mihpayid')
    amount = response['return_data'].get('amount')
    case_id = response['return_data'].get('productinfo').split('-')[2]

    if case_id != '':
        case = Case.objects.get(id=case_id)
        case.total_online += float(amount)
        case.has_finished
        case.save()
    else:
        case = None

    user = AccountUser.objects.filter(email=response['return_data'].get('email')).first()

    donation = ProjectDonation.objects.create(
        donor=user,
        full_name=f'{firstname} {lastname}',
        email=email,
        phone_number=phone,
        address=address,
        state=state,
        city=city,
        category=category,
        country=country,
        gender=gender,
        pan=pan,
        transaction_id=trans_id,
        amount=amount,
        case=case
    )

    donation.save()

    # context = {'donation': donation, 'case': case, 'static_root': str(settings.STATIC_URL)}
    # html_string = render_to_string('projects/invoice.html', context)
    #
    # pdf_file = HTML(string=html_string).write_pdf(stylesheets=[
    #     CSS(settings.STATIC_URL + 'media/assets/css/argon.min.css')
    # ])
    # response = HttpResponse(pdf_file, content_type='application/pdf')
    # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    #
    # # send_email_invoice(donation=donation, pdf=pdf_file)
    # if donation.case is not None:
    #     case = donation.case.title
    # else:
    #     case = f'{donation.category}'
    #
    # msg = EmailMessage(
    #     f'Invoice #00{donation.id} for {donation.amount} Donation for {case}',
    #     pdf_file,
    #     'igetbangalore@gmail.com',
    #     [donation.email],
    # )
    # msg.content_subtype = "pdf"  # Main content is now text/html
    # msg.encoding = 'ISO-8859-1'
    # # email.send()
    # # msg.attach(pdf_file)
    # msg.send()

    context = {'trans_id': trans_id, 'amount': amount, 'case_id': case_id}

    return render(request, 'projects/success.html', context)


@csrf_exempt
def failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return HttpResponse('Sorry, something went wrong. Please try again later')


# TODO remove before pushing it
def pdf_test_w(request):
    case = Case.objects.all().first()
    donation = ProjectDonation.objects.filter(case=case, full_name='Imran Rahman').first()
    context = {'donation': donation, 'case': case, 'static_root': str(settings.STATIC_URL)}
    html_string = render_to_string('projects/invoice.html', context)

    pdf_file = HTML(string=html_string).write_pdf(stylesheets=[
        CSS(settings.STATIC_URL + 'media/assets/css/argon.min.css')
    ])
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'

    return response