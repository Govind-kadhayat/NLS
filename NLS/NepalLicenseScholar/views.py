from django.shortcuts import render,HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("this is Home page ")

def about(request):
    return HttpResponse("this is About page ")


def contact(request):
    return HttpResponse("this is contact page ")

