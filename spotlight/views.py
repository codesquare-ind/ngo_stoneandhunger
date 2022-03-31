from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import MediaSpotlight, SpotlightImages
from account.decorators import allowed_roles


def media(request):
    spotlights = MediaSpotlight.objects.all().order_by('-date_published')
    context = {'spotlights': spotlights}
    return render(request, 'spotlight/index.html', context)


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def add_media(request):
    if request.method == 'POST' and request.FILES.getlist('images'):
        images = request.FILES.getlist('images')
        title = request.POST.get('title')
        link = request.POST.get('link')
        date = request.POST.get('date_published')
        description = request.POST.get('description')

        spotlight = MediaSpotlight.objects.create(title=title, link=link, date_published=date, description=description)
        spotlight.save()

        for img in images:
            p = SpotlightImages.objects.create(image=img, media=spotlight)
            p.save()

    return redirect('a_media')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def del_img_set(request, pk):
    s = MediaSpotlight.objects.get(id=pk)
    for img in s.spotlightimages_set.all():
        img.delete()
    s.delete()
    return redirect('a_media')


@login_required(login_url='login')
@allowed_roles(roles=['admin'])
def del_img(request, pk):
    img = SpotlightImages.objects.get(id=pk)
    img.delete()
    return redirect('a_media')


@login_required(login_url='login')
@allowed_roles(roles=['admin', 'subadmin'])
def add_new_images(request, pk):
    img_set = MediaSpotlight.objects.get(id=pk)

    if request.method == 'POST' and request.FILES['images']:
        images = request.FILES.getlist('images')

        for img in images:
            p = SpotlightImages.objects.create(image=img, media=img_set)
            p.save()

        return redirect('a_media')