from django.shortcuts import render,HttpResponse

# Create your views here.

def home(request):
    return render(request,'home.html')

def about(request):
    return render( request,"about.htlm")


def contact(request):
    return render(request,"contact.html")


def dashboard(request):
    return render(request,"dashboard.html")
