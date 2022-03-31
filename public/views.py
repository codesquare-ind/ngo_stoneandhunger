from django.core.mail import EmailMessage
from django.db.models import Q
from django.shortcuts import render
from projects.models import Case
from .models import ImageSet, Photo


def pg_not_found_error(request, exception):
    return render(request, 'public/404.html')


def index(request):
    top_cases = Case.objects.filter(status='Green').order_by('priority', '-date_of_initiation')[:3]
    context = {
        'top_cases': top_cases
    }
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        msg = EmailMessage(
            'Contact mail by {}'.format(str(name)),
            '{} from {} the contact email sent this message: {}'.format(str(name), str(email), str(message)),
            'igetbangalore@gmail.com',
            ['igetbangalore@gmail.com'],
        )
        msg.send()
    return render(request, 'public/index.html', context)


def contact(request):
    return render(request, 'public/contact.html')


def about(request):
    return render(request, 'public/about.html')


def gallery(request):
    img_sets = ImageSet.objects.all().order_by('-date_created__date')
    context = {'img_sets': img_sets}
    return render(request, 'public/gallery.html', context)


def terms(request):
    return render(request, 'public/terms.html')


def policy(request):
    return render(request, 'public/privacy_policy.html')