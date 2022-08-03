from unicodedata import category
import uuid
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import os

from numpy import iterable
# Create your models here.


def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images', filename)


class Images2(models.Model):
    First_name=models.CharField(max_length=100)
    second_name=models.CharField(max_length=100)
    Patient_id=models.IntegerField(primary_key=False)
    image_id=models.IntegerField(primary_key=True)
    category = models.CharField(max_length=400)
    # title = models.CharField(max_length=250)
    image = models.ImageField(
        upload_to=user_directory_path, default='posts/default.jpg')
    image_date= models.CharField(max_length=250)
####################################

class Item(models.Model):
    Name = models.TextField(max_length=191, null=False)
    category = models.TextField(max_length=50,  null=True)
    Date = models.TextField(max_length=500, null=True)
    image = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
    patientid= models.TextField( null=False)
    imageid=models.BigAutoField(primary_key=True)
    notes=models.TextField(max_length=500,  null=True)


####
class doctor(models.Model):
    Name = models.TextField(max_length=191,  null=False)
    docid = models.TextField(max_length=50,  null=False)

class RoomMember(models.Model):
    name=models.CharField(max_length=200)
    uid=models.CharField(max_length=200)
    room_name=models.CharField(max_length=200)

    def __str__(self):
        return self.name

