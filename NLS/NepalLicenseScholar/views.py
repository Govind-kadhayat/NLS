from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render
from datetime import datetime
from.models import *
import random

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

    # data = Signup.objects.all()
    contex = {'categories':Category.objects.all()}

    # user = {
    #     'data':data,}

    
    return render(request,"notice.html",contex)





def get_quiz(request):
    try:
        question_objs = list(Question.objects.all())
        data =[]
        random.shuffle(question_objs)

        for question_obj in question_objs:
            data.append({
                "Category": question_obj.Category.category_name,
                "question":question_obj.question,
                "marks":question_obj.marks,
                "ansswer":question_obj.get_answer()
         })


        payload = {'status':True,'data':data}
        return JsonResponse(payload)

    except Exception as e:
        print(e)
    return HttpResponse("Some thing went wrong")


def side_bar(request):
        return render(request,"main/side_bar.html")