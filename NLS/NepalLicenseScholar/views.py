from django.shortcuts import render,HttpResponse
from datetime import datetime
from NepalLicenseScholar.models import Contact
from NepalLicenseScholar.models import Signup

# Create your views here.

def home(request):
    return render(request,'home.html')

def about(request):
    return render( request,"about.htlm")

def contact(request):
      if request.method == "POST":
         name = request.POST.get('name')
         email = request.POST.get('email')
         phone = request.POST.get('phone')
         address= request.POST.get('address')
         desc = request.POST.get('desc')
         new_contact = Contact(
            name=name,
            email=email,
            phone=phone,
            address=address,
            desc=desc,
            date=datetime.now()  
        )
         new_contact.save()


  
      return render(request,'contact.html')



def dashboard(request):
    return render(request,"dashboard.html")

def login(request):
    return render(request,"login.html")

def register(request):
    if request.method == "POST":
         name = request.POST.get('name')
         email = request.POST.get('email')
         password = request.POST.get('password')
         phone = request.POST.get('phone')
         address= request.POST.get('address')
         date=datetime.now()
         signup = Signup(
            name=name,
            email=email,
            password = password,
            phone=phone,
            address=address,
            date=datetime.now()  
        )
         signup.save()


    return render(request,"register.html")

def notice(request):

    data = Signup.objects.all()

    user = {
        'data':data,

    }
    return render(request,"notice.html",user)