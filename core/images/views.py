# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from sqlite3 import Date
from tokenize import Name
from cv2 import QRCodeDetector
from dateutil.parser import parse
import cv2
from matplotlib import image
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from PIL import Image
import pytesseract
from skimage.color import label2rgb, rgb2gray
import glob
import dateutil.parser as dparser
from datetime import datetime
import re
import datefinder
from reportlab.lib.utils import ImageReader
from unidecode import unidecode
import datefinder
from pygrok import Grok
from pytesseract import Output
import csv
import re
from PIL import Image, ImageChops
from scipy.spatial import distance as dist
import easyocr
from easyocr import Reader
import torch
import os
import sys
from textblob import TextBlob
import unicodedata
from datetime import date
import colorama
from colorama import Fore, Style
from pyzbar.pyzbar import decode
import convert_numbers
import datetime
from bidi.algorithm import get_display
import gc
import os
import pandas as pd 
# Create your views here.
from pyexpat import model
from unicodedata import category, name
from django.forms import modelformset_factory
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
# from matplotlib import image
from rest_framework.decorators import api_view
from agora_token_builder import RtcTokenBuilder,RtmTokenBuilder
import random
import time
import json
from .models import RoomMember
# from matplotlib import image
from rest_framework.decorators import api_view
from core.settings import BASE_DIR
# import images
# from images.form import ImagefieldForm
from .models import Item, doctor
from.serialztion import ImagesofItem
from rest_framework.response import Response
from rest_framework import status,filters
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import Item
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.exceptions import SuspiciousOperation



date_string = ['/', '\\', '-']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
             'August', 'September', 'October', 'November', 'December']
cnts = []
res = []
date1 = []
num = 0  
kernel = np.ones((2, 2), np.uint8)
       

@api_view(['GET','POST'])
def upload (request):
     if request.method == "GET":
            data_of_images = Item.objects.all()
            serializer = ImagesofItem(data_of_images, many=True)
            return Response(serializer.data)
     elif request.method=='Post': 

         serializer= ImagesofItem(data=request.data)
         if serializer.is_valid():
             serializer.save()
             return Response(request, status=status.HTTP_201_CREATED)
         return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)



###################################
def guess_date(string):

    for fmt in ["%d%m%Y", "%d-%m-%Y", "%Y/%m/%d"]:
        try:
            d = datetime.datetime.strptime(string, fmt).date()
            return d.strftime("%d-%m-%Y")
        except ValueError:
            continue
    raise ValueError(string)        
##################################

def temporary_file_path(self):
   
    return self.file.name

def back(str):
    st2=''
    for i in range(len(str)-1,-1,-1):
        st2+=str[i]
    return st2

###############################

def addProduct(request):
    if request.method == "POST":
        prod = Item()

        global z
        z=""
        global x
        x=""
        date1.clear()
        files = request.FILES.getlist('image')
        if len(files) != 0:
            for f in files:
                im =f
                kernel_bar = np.ones((5, 5), np.uint8)
                ttt=temporary_file_path(f)
                im2 = cv2.imread(ttt)
                im3 = cv2.imread(ttt)
                barcodes = []   
                im4 = np.copy(im)
                im_for_barcode = np.copy(im)
                im_for_barcode=image.imread(im)
                im_for_barcode = cv2.cvtColor(im_for_barcode, cv2.COLOR_BGR2GRAY)
                im_for_barcode = cv2.erode(im_for_barcode, kernel_bar, iterations=1)
                barcodes.append(decode(im_for_barcode))
                barcodes = [ele for ele in barcodes if ele != []]
                for barcode in barcodes:
    
                    bdata = barcode[0].data.decode("utf-8")
                    barcode_text = f"{bdata}"
                    if (barcode_text == 'AB0011401'):
                        xc1="Patient Initial Data"
                        prod.category =xc1
                    elif(barcode_text == "AC0021302"):
                        xc2 = "Initial Assment"
                        prod.category =xc2
                    elif(barcode_text == 'AD0031203'):
                        xc3 = "Breast-Imaging"
                        prod.category =xc3
                    elif(barcode_text == 'AE0041104'):
                        xc4 = "Genral-Radioloy"
                        prod.category =xc4            
                    elif (barcode_text == 'AF0051005'):
                        xc5="Pet-Scan" 
                        prod.category =xc5 
                    elif(barcode_text == 'AG0060906'):
                        xc6 = "Pathology"
                        prod.category =xc6    
                    elif(barcode_text == 'BC0070807'):
                        xc7 = "Tumor-Board"
                        prod.category =xc7 
                    elif(barcode_text == 'BD0080708'):
                        xc8 = "Clinic-Visits"
                        prod.category =xc8
                    elif(barcode_text == 'BE0090609'):
                        xc9 = "Reports&Consents" 
                        prod.category =xc9
                    elif(barcode_text == 'BF0100510'):
                        xc10 = "Operative-Sheets"
                        prod.category =xc10
                    elif(barcode_text == 'BG0110411'):
                        xc11 = "Labs"
                        prod.category =xc11 
                    elif(barcode_text == 'CD0120312'):
                        xc12 = "Cardiac-clinic" 
                        prod.category =xc12
                    elif(barcode_text == 'CE0130213'):
                        xc13 = "Others" 
                        prod.category =xc13
                    else:
                        xc14 = "UnKnown Cateogry" 
                        prod.category =xc14        
                ############################################################
                prod.Name = request.POST.get('Name')
                prod.patientid = request.POST.get('patientid')
                z1=prod.patientid

                kernel = np.ones((2, 2), np.uint8)
                img=cv2.imread(ttt)


                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                mask = (cv2.inRange(img, (90, 50, 38), (110, 255, 255)))
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                contours, hierarchy = cv2.findContours(
                    mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
                
                   
                for j in contours:
                    area = cv2.contourArea(j)
                    print(area) 
                    if (area > 10000):
                        x, y, w, h = cv2.boundingRect(j)
                        cv2.rectangle(im2, (x, y), (x + w, y + h),
                                        (255, 36, 12), 10)
                        im2[y:y+h, x:x+w]
                        cnts.append(j)                        
                height, width, _ = im2.shape
                min_x, min_y = width, height
                max_x = max_y = 0
                for c in cnts:
                    (x, y, w, h) = cv2.boundingRect(c)
                    min_x, max_x = min(x, min_x), max(x+w, max_x)
                    min_y, max_y = min(y, min_y), max(y+h, max_y)
                    if w > 80 and h > 80:
                        cv2.rectangle(im3, (x, y), (x+w, y+h),
                                        (255, 255, 255), 10)
                if max_x - min_x > 0 and max_y - min_y > 0:
                    cv2.rectangle(im3, (min_x, min_y),
                                    (max_x, max_y), (0, 0, 255), 10)
                    result = im3[min(min_y, max_y):max(
                        min_y, max_y), min(min_x, max_x):max(min_x, max_x)]
                    
                    kernel_date = np.ones((3, 3), np.uint8)
                    im_for_date = cv2.erode(result, kernel_date, iterations=1)
                    
                    reader = easyocr.Reader(['en', 'ar'])
                    read = reader.readtext(im_for_date)
                    for ele in read:
                        for item in ele:
                            if (type(item) != list):
                                if (type(item) != np.float64):
                                    date1.append(item)
                                    print(date1)
#############################################################################################                                            
                for m in months:
                    for t in date1:

                        if(m in t):
                            x1 = t.replace("January", "-01-").replace("February", "02").replace("March", "03").replace("April", "04").replace("May", "05").replace("June", "06").replace(
                                "July", "07").replace("August", "08").replace("September", "-09-").replace("October", "10").replace("November", "11").replace("December", "12").replace(" ", "-").replace(" ", "")
                            x1=x1.replace("f","").replace("th","").replace("t","").replace("h","")
                            matches = list(datefinder.find_dates(x1))
                            print("matches",matches[0])
                            x=matches[0].strftime('%d-%m-%Y')
                            prod.Date = x  
                            # Item.objects.create(Date=x)

                for a in date_string:
                    for b in date1:
                        try:
                           
                            if ((a in b) and parse(b, fuzzy=True, dayfirst=True)):
                                ######################################### Formats ###########################################################################
                                x =b
                                x = get_display(x)
                                x = x.replace("/", "-").replace("\\","-").replace(".", "-").replace("//", "-")
                                mat = list(datefinder.find_dates(x[0]))

                                print("mat",mat)
                                x= datetime.datetime.strptime(str(mat), '%d-%m-%Y')
                                print("x",x)


                                # Item.objects.create(Date=x)
                             
                                      
                        except ValueError:
                            continue
                #############################

                
                
                no1="١/"
                no2="٢/"
                no3="٣/"
                no4="٤/"
                no5="٥/"
                no6="٦/"
                no7="٧/"
                no8="٨/"
                no9="٩/"
                no10="١٠/"
                no11="١١/"
                no12="١٢/"
                ###
                no1.encode("utf-8")
                no2.encode("utf-8")
                no3.encode("utf-8")
                no4.encode("utf-8")
                no5.encode("utf-8")
                no6.encode("utf-8")
                no7.encode("utf-8")
                no8.encode("utf-8")
                no9.encode("utf-8")
                no10.encode("utf-8")
                no11.encode("utf-8")
                no12.encode("utf-8")
                #####
                for ara in date1:
                    ara.encode("utf-8")  
                    if (no1 in ara or no2 in ara or no3 in ara  or no4 in ara  or no5 in ara  or no6 in ara  or no7 in ara  or no8 in ara  or no9 in ara  or no10 in ara  or no11 in ara or no12 in ara): 
                        ara = ara.replace(" ","")               
                        x1=(unidecode(ara))   
                        print(x1)                
                        x1 = x1.replace(" ","")
                        x=back(x1)
                        x = x.replace(" ","").replace("/", "-").replace("\\","-").replace(".", "-").replace("//", "-")
                        x= datetime.datetime.strptime(x, '%Y-%m-%d')
                        x = x.strftime("%d-%m-%Y")


                ######################                
                # print("Final x ")
                # print(x)
                notes = request.POST.get('notes', None)
                prod.notes=notes
                Item.objects.create(image=f,Date=x,category=prod.category,Name=prod.Name,patientid=z1, notes=prod.notes)
                date1.clear()
          

    return render(request, 'project/addingPage.html')




def updatepage(request):
    # name = request.POST.get('name', None)
    if request.method == "POST":
        date = request.POST.get('date', None)
        cat = request.POST.get('cat', None) 
        imageid= request.POST.get('imageid') 
        #####
        Item.objects.filter(imageid__exact=imageid).update(Date=date,category=cat) 
        id=Item.objects.filter(imageid__exact=imageid)
        for m in id:
            m.image = request.FILES['image']
            m.save() 
           
    return render(request, 'project/updatepage.html')    

def show(request):


    if request.method == "POST":
        # searched = request.POST['searched']
        searched = request.POST.get('searched', None) 
        # a=Item.objects.all()

        if searched is not None:
            venus=Item.objects.filter(patientid__exact=searched).order_by('Date')
            return render(request, 'project/showData.html', {'searched' : searched, 'venus': venus})
        else:    
            messages.error(request,"Not Results Found , Please check the Patient-ID") 
        return redirect('.') 


    return render(request, 'project/showData.html')



def cat_delete(request, id):
    
    cat=Item.objects.get(imageid=id)
    if request.method == 'POST':         # If method is POST,   
        cat.delete()                     # delete the cat.
        return redirect('show')
       
       
    return render(request, 'project/showData.html') 



    
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        # myuser = User.objects.create_user(username, email, pass1)
        # myuser.save()
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('.')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('.')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('.')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('.')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('.')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        return redirect('patientdata')

    return render(request,'project/signUp.html',{})    

def signin(request):
    if request.method == 'POST':

        username=request.POST['username']
        pass1=request.POST['pass1']
        user= authenticate(request, username=username, password=pass1)
        # print(email)
        # print(pass1)
    
        if user is not None:
            login(request,user)
            return render(request,"project/patientData.html",{"username":username})
        else:  
            messages.error(request,"Bad crendentials") 
        return redirect('.') 

    return render(request, 'project/signIn.html')  


def patientData(request):
    



    return render(request, 'project/patientData.html')   





def index(request):
    return render(request, 'project/index.html')  


def doctorsignin(request):

    if request.method == "POST":

        username = request.POST.get('username', None)
        pass1 = request.POST.get('pass1', None)


        if pass1 is not None:

            venus=doctor.objects.filter(docid__exact=pass1 , Name__exact=username)

            if  venus.count()!= 0:

            
                return  redirect('doctorview')
        else:

            
            messages.error(request,"Not Results Found , Please check the Patient-ID") 
            return redirect('doctorsignin') 

    return render(request, 'project/doctor_signin.html')  



def deletedoctor(request):

    dele=doctor()
    Name=request.POST.get('Name', None)
    docid=request.POST.get('docid', None)
    if request.method == "POST":
        venus=doctor.objects.filter(docid__exact=docid , Name__exact=Name)
        venus.delete()
    # else:
    #     messages.error(request,"Not vaild") 
    #     return redirect('deletedoctor')

    return render(request, 'project/deletedoctor.html') 

def forget(request):
    


    return render(request, 'project/forget.html') 




def patientsignin(request):

 


    if request.method == "POST":
        patientname = request.POST.get('patientname', None)
        pass1 = request.POST.get('pass1', None)

  
        
        if pass1 is not None:
            venus=Item.objects.filter(patientid__exact=pass1 , Name__exact=patientname)
            
            if   venus.count() != 0:
            
                return render(request, 'project/patient_view.html', {'venus' : venus})
                
        else:    
            
            messages.error(request,"Not Results Found , Please check the Patient-ID") 
            return redirect('patientsignin') 


    
    return render(request, 'project/patient_signin.html')  






def patientview(request):
    if request.method == "POST":
        # searched = request.POST['searched']
        searched = request.POST.get('searched', None) 
        # a=Item.objects.all()

        if searched is not None:
            venus=Item.objects.filter(patientid__exact=searched).order_by('Date')
            return render(request, 'project/patient_view.html', {'searched' : searched, 'venus': venus})
        else: 
            messages.error(request,"Not Results Found , Please check the Patient-ID") 
            return redirect('.') 
    return render(request, 'project/patient_view.html') 






def patientupload(request):
    category = request.POST.get('category', None)
    Name = request.POST.get('Name', None)
    Date = request.POST.get('Date', None)
    patientid = request.POST.get('patientid', None)


    if request.method == "POST":
        prod = Item()
        files = request.FILES.getlist('image')
        if len(files) != 0:
            for f in files:
                prod.category= category
                prod.image= f
                prod.Name=Name
                prod.Date=Date
                prod.patientid=patientid
                Item.objects.create(image=f,Date=prod.Date,category=prod.category,Name= prod.Name,patientid= prod.patientid)        



    return render(request, 'project/patient_upload.html') 

def doctorview(request):
    
        if request.method == "POST":
            # searched = request.POST['searched']
            searched = request.POST.get('searched', None) 
        # a=Item.objects.all()

            if searched is not None:
                venus=Item.objects.filter(patientid__exact=searched).order_by('Date')
                return render(request, 'project/doctor_view.html', {'searched' : searched, 'venus': venus})
            else:    
                messages.error(request,"Not Results Found , Please check the Patient-ID") 
            return redirect('.') 

        return render(request, 'project/doctor_view.html') 
    
    
def deletepatient(request):

    if request.method == "POST":

       
        searched = request.POST.get('searched', None) 

        if searched is not None:
            venus=Item.objects.filter(patientid__exact=searched).order_by('Date')
            venus.delete()
            return render(request, 'project/showData.html', )
        else:    
            messages.error(request,"Not Results Found , Please check the Patient-ID") 
            return redirect('.')     
    
    return render(request, 'project/showdata.html') 
    
      










def index2(request):

    if request.method == "POST":
        searched = request.POST['searched']

        if searched is not None:
            venus=Item.objects.filter(patientid__contains=searched).order_by('Date')
            
            return render(request, 'project/index2.html', {'searched' : searched, 'venus': venus})
        else:    
            messages.error(request,"Not Results Found , Please check the Patient-ID") 
        return redirect('.') 
    

    return render(request, 'project/index2.html')




def adddoctor(request):

    dr=doctor()
    Name = request.POST.get('Name', None)
    docid= request.POST.get('docid', None)
    if request.method == "POST":

        dr.Name= Name
        dr.docid=docid
        doctor.objects.create(Name= dr.Name, docid= dr.docid)   

    return render(request, 'project/adddoctor.html') 








def pdf(request):
    # from reportlab.pdfgen.canvas import Canvas
  
    # buffer = io.BytesIO()
    # global read
    # global c
    # c = canvas.Canvas(buffer)
    # if request.method == "POST":
    #     searched = request.POST.get('searched', None) 
    #     if searched is not None:
    #         venus=Item.objects.filter(patientid__exact=searched).order_by('Date')
    #         image_list = venus.values_list('image',flat = True)
    #         for v in image_list:
    #             read =ImageReader(v)
    
    #     c.drawImage(read, 10, 10, mask='auto')
    #     c.showPage()
    #     c.save()
    #     buffer.seek(io.SEEK_SET)
    from fpdf import FPDF
    pdf = FPDF()
    global imagelist
    imagelist=[]
    if request.method == "POST":
        searched = request.POST.get('searched', None) 
        if searched is not None:
            venus=Item.objects.filter(patientid__exact=searched).order_by('Date')
            for v in venus:
                imagelist.append(v.image)

    import tifffile

    for image in imagelist:
        pdf.add_page()
        tifffile.imread(pdf.image(image.path))
    pdf.output("yourfile.pdf", "F")

    return render(request, 'project/showdata.html')
           

# ---------------------------start video conference-------------------------
# get video channel token and generate user id
def getToken(request):
    
    appId='8965c2ff3d7c47e2be1d23e5a000273d'
    appCertificate='87ff45753b584dea8610570dc8d3f393'

    channelName=request.GET.get('channel')
    userName=request.GET.get('name')
    uid=userName+'-'+str(random.randint(1,230))
    expirationTimeInSeconds=3600*24
    # to let the user know when the time of the session will be expired
    currentTimeStamp=time.time() #what is the time right now
    privilegeExpiredTs=currentTimeStamp+expirationTimeInSeconds
    role=1 #like one host
    print('uid:',uid)
    rtcToken = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    rtmToken = RtmTokenBuilder.buildToken(appId, appCertificate, uid, role, privilegeExpiredTs)
    return JsonResponse({'rtcToken': rtcToken,'rtmToken':rtmToken, 'uid': uid}, safe=False)


def lobby(request):
    return render(request,'project/lobby.html')

def room(request):
    return render(request,'project/room.html')

def createUser(request):
    data = json.loads(request.body)
    member,created=RoomMember.objects.get_or_created(
        name=data['name'],
        uid=data['UID'],
        room_name=data['room_name']
        )
    return JsonResponse({'name':data['name']},safe=False)
# ---------------------------end video conference-------------------------




    




    
        




