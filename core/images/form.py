import uuid
from django import forms 
from django.contrib.auth.models import User
import os
from django.utils import timezone

# from images.models import Images2

# class ImagefieldForm(forms.ModelForm): 
#     class Meta:
#         model=Images2
#         images =forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    
    # def user_directory_path(instance, filename):
    #     ext = filename.split('.')[-1]
    #     filename = "%s.%s" % (uuid.uuid4(), ext)
    #     return os.path.join('images', filename)

    # # img_category = forms.CharField()
    # img_firstname = forms.CharField()
    # img_secondname = forms.CharField()
    # img_patientid = forms.IntegerField()
    # img_imageid=forms.IntegerField()
    # img_image=forms.ImageField()
    # date_image=forms.CharField()

