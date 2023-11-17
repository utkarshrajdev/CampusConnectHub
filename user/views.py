from django.shortcuts import render, redirect
from django.http import HttpResponse
from .scrap import *
from .studyguide import *
from .models import *
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from itertools import chain
from django.core.paginator import Paginator
import datetime
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

# // Config
cloudinary.config(
  cloud_name = "dzqr5mmwt",
  api_key = "263454863926658",
  api_secret = "5DfZPkgxd7VM0P1Drp9Sk-vAM9A",
  secure = True
)

def login(request):
  if request.method == 'POST' :
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None :
      auth_login(request, user)
      return redirect('/showcolleges')
    else:
      return HttpResponse("Invalid Credentials OR You are not approved by the admin yet.")
  return render (request, 'login.html')

def showcolleges(request):
    if request.user.is_authenticated :
        u = Employee.objects.get(username=request.user.username)
        query = request.GET.get('p')
        states = u.state
        states = states.split(',')
        colleges = College.objects.none()
        for state in states :
          try:
            temp = College.objects.all().filter(state=state)
            colleges = chain(colleges, temp)
          except:
             pass
        colleges = list(colleges)
        colleges = College.objects.filter(id__in=[obj.id for obj in colleges])
        object_list = []
        if (query == None):
          object_list = list(colleges)
        else:
              Collegename_list=colleges.filter(name__icontains=query)
              City_list=colleges.filter(city__icontains=query)
              State_list=colleges.filter(state__icontains=query)
              for i in Collegename_list:
                  object_list.append(i)
              for i in City_list:
                  if i not in object_list:
                      object_list.append(i)
              for i in State_list:
                  if i not in object_list:
                      object_list.append(i)
        object_list = list(object_list)
        college_paginator = Paginator(object_list, 30)
        page_num = request.GET.get('page')
        print(page_num)
        page = college_paginator.get_page(page_num)
        surl = request.get_full_path()

    # Append the search query to the URL as a query parameter
        if query:
            surl += '&'
        else :
           surl = '/showcolleges?'
        allfollowup =  Followup.objects.all()
        context = {'u': u,'page': page,'query': query,'surl': surl,'followup': allfollowup}
        return render (request,'showcolleges.html',context)
    else :
        return redirect('/login')

def CollegeSearchView(request):
   if request.user.is_authenticated :
    query = request.GET.get('p')
    object_list = []
    if (query == None):
          object_list = College.objects.all()
    else:
          Collegename_list=College.objects.filter(name__icontains=query)
          City_list=College.objects.filter(city__icontains=query)
          State_list=College.objects.filter(state__icontains=query)
          for i in Collegename_list:
              object_list.append(i)
          for i in City_list:
              if i not in object_list:
                  object_list.append(i)
          for i in State_list:
              if i not in object_list:
                  object_list.append(i)
    
    allfollowup =  Followup.objects.all()
    print(allfollowup)
    context = {
    'colleges': object_list,
    'query': query, 'followup': allfollowup
    }
    return render (request,'showcolleges.html',context) 
   else :
    return redirect('/login')
    

def register(request):
    if  request.user.is_authenticated and request.user.is_staff :
      u = Employee.objects.get(username=request.user.username)
      if request.method == 'POST' :
        name = request.POST['name']
        fathername = request.POST['fathername']
        mobile = request.POST['mobile']
        gender = request.POST['gender']
        aadhar = request.POST['aadhar']
        username = request.POST['username']
        email = request.POST['email']
        password = username + "@123"
        selectedstates = request.POST.getlist('selectedstates')
        selectedstates = ','.join(selectedstates)
        n = Employee(name=name, username=username, fathername = fathername, mobile = mobile,
                     gender = gender, aadhar = aadhar, email=email, state=selectedstates)
        n.set_password(password)
        n.save()
        redirect('/register')
      states = State.objects.all()
      context = {'u': u,'states': states}
      return render (request,'register.html',context)
    else :
      return redirect('/login')
    
def savefollowup(request):
    if  request.user.is_authenticated :
      if request.method == 'POST' :
        collegeid = request.POST['collegeid']
        message = request.POST['message']
        current_date = datetime.datetime.now().strftime('%Y-%m-%d')
        current_time = datetime.datetime.now().strftime('%H:%M:%S')
        ins = Followup(collegeid=collegeid, message=message, date=current_date, time=current_time)
        ins.save()
        return redirect('/showcolleges')
    else :
      return redirect('/login')

def editcollegedetails(request) :
   if request.method == 'POST' :
    id = request.POST['id']
    c = College.objects.get(id=id)
    c.name = request.POST['name']
    c.city = request.POST['city']
    c.state = request.POST['state']
    c.phone = request.POST['phone']
    c.email = request.POST['email']
    c.website = request.POST['website']
    category = request.POST['category']
    if category == "":
        c.category = None
    else:
        c.category = category
    courses = request.POST.getlist('courses[]')
    if not courses:
        courses = None
    c.courses = courses
    c.save()
    return redirect('/showcolleges')


def logout(request):
  auth_logout(request)
  return redirect('/login')


def changepassword(request):
  if  request.user.is_authenticated :
    user = Employee.objects.get(email=request.user.email)
    context = {'u': user}
    if request.method == 'POST' :
          password = request.POST['new_password']
          user.set_password(password)
          user.save()
          return redirect('/showcolleges')
    return render (request, 'changepassword.html', context) 
  else :
    return redirect('/login')
  



def editprofile(request):
    if  request.user.is_authenticated :
      u = Employee.objects.get(username=request.user.username)
      if request.method == 'POST' :
        u.name = request.POST['name']
        u.fathername = request.POST['fathername']
        u.mobile = request.POST['mobile']
        u.gender = request.POST['gender']
        u.aadhar = request.POST['aadhar']
        u.username = request.POST['username']
        u.email = request.POST['email']
        try :
          profileimage = request.FILES['profileimage']
          cloudinaryname = u.username+str(u.id)
          upload(profileimage, public_id=cloudinaryname)

          # // Transform
          url, options = cloudinary_url(cloudinaryname, width=100, height=100, crop="fill")
          u.imageurl = url
        except :
           pass
        u.save()
        redirect('/showcolleges')
      context = {'u': u,'user':u,}
      return render (request,'editprofile.html',context)
    else :
      return redirect('/login')