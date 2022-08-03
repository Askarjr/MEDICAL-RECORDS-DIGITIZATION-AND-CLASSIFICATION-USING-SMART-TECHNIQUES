"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from unicodedata import name
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from images.views import addProduct, deletedoctor, forget,upload,show,signup,signin,index, patientData, index2,cat_delete,updatepage,doctorsignin,patientsignin,patientupload,patientview,doctorview,adddoctor, deletedoctor,lobby,room, forget,deletepatient
from images import views
# from django.urls import re_path as url
# from django.contrib import admin
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('add', addProduct, name='add'),  
    path('database/',show, name= 'show'),
    path('list/',upload),
    path('signin/',signin, name='signin'),
    path('signup/',signup, name='signup'),
    path('patientdata/',patientData, name='patientdata'),
    path('index/',index, name='index'),
    path('index2/',index2, name='index2'),
    path('database/delete/<id>/', cat_delete, name='cat_delete'),
    path('updatepage/', updatepage, name='updatepage'),
    path('doctorsignin/', doctorsignin, name='doctorsignin'),
    path('patientsignin/', patientsignin, name='patientsignin'),
    path('doctorview/', doctorview, name='doctorview'),
    path('patientview/', patientview, name='patientview'),
    path('patientupload/', patientupload, name='patientupload'),
    path('adddoctor/', adddoctor, name='adddoctor'),
    path('deletedoctor/', deletedoctor, name='deletedoctor'),
    path('lobby/',lobby, name='lobby'),
    path('room/',room,name='room'),
    path('get_token/', views.getToken),
    path('forget/',forget, name='forget'),
    path('deletepatient/',deletepatient, name='deletepatient'),
   
    # path('deletepatient/<id>',deletepatient, name='deletepatient'),
   

    # path('le/',addpage),
   

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

