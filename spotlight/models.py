from django.db import models


class MediaSpotlight(models.Model):
    title = models.CharField(max_length=250, null=True)
    link = models.CharField(max_length=250, null=True, blank=True)
    date_published = models.DateTimeField(auto_now_add=False, null=True)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


class SpotlightImages(models.Model):
    media = models.ForeignKey(MediaSpotlight, null=True, on_delete=models.CASCADE)
    image = models.ImageField(null=True)