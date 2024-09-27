from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
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
    return render(request,"notice.html")


def get_quiz(request):
    try:
        question_objs = Question.objects.all()
        
        
        if request.GET.get('category'):

            category_filter = request.GET.get('category')
            
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))

        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)  
      
        for question_obj in question_objs:
            data.append({
                "Category": question_obj.category.category_name,  
                "question": question_obj.question, 
                "marks": question_obj.marks,  
                "Answer": question_obj.get_answer(),  
            })

        payload = {'status': True, 'data': data}
        return JsonResponse(payload)  

    except Exception as e:
        print(e) 
        return HttpResponse("Something went wrong")  

def side_bar(request):
        return render(request,"main/side_bar.html")

def profile(request):
        return render(request,"main/profile.html")

def study(request):
        return render(request,"main/study.html")
def tax(request):
        return render(request,"tax.html")

def test(request):
        context = {'categories':Category.objects.all()}
        if request.GET.get('category'):
            return redirect(f"/testq/?category={request.GET.get('category')}")
        return render(request,"test.html",context)


def testq(request):
    
    return render(request ,"testq.html")
