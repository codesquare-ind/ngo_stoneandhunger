from django.db import models


class ImageSet(models.Model):
    title = models.CharField(max_length=150, null=True)
    description = models.CharField(max_length=250, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)


class Photo(models.Model):
    image = models.ImageField(null=True, blank=True)
    set = models.ForeignKey(ImageSet, null=True, on_delete=models.CASCADE)