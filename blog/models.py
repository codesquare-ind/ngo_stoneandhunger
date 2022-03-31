import uuid as uuid
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import AccountUser
import uuid


class BlogPost(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, null=True)
    thumbnail = models.ImageField(null=True, blank=True)
    title = models.CharField(max_length=250, null=True)
    overview = RichTextUploadingField(null=True)
    posted_on = models.DateTimeField(auto_now_add=True, null=True)
    posted_by = models.ForeignKey(AccountUser, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Comment(models.Model):
    class Meta:
        ordering = ['-posted_on']

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, null=True)
    comment = models.CharField(max_length=500, null=True)
    posted_by = models.ForeignKey(AccountUser, null=True, on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True, null=True)