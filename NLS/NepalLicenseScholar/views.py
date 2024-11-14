from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from.models import *
import re
import json
import random

# Home Page
def home(request):
    return render(request, 'home.html')

# About Page
def about(request):
    return render(request, "about.html")

# Contact Page
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
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
    return render(request, 'contact.html')

# Dashboard Page
def dashboard(request):
    return render(request, "dashboard.html")

# Login View
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

# Registration View
def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # Validation
        if not name or not email or not password or not phone or not address:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return render(request, "register.html")

        if Signup.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "register.html")

        if not re.match(r'^\d{10}$', phone):
            messages.error(request, "Enter a valid 10-digit phone number.")
            return render(request, "register.html")

        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, "register.html")

        # Save User
        signup = Signup(name=name, email=email, password=password, phone=phone, address=address, date=datetime.now())
        signup.save()
        messages.success(request, "Registration successful!")
        return redirect('login')
    return render(request, "register.html")

# Notice Page
def notice(request):
    return render(request, "notice.html")

# Quiz Data
def get_quiz(request):
    try:
        question_objs = Question.objects.all()
        
        if request.GET.get('category'):
            category_filter = request.GET.get('category')
            question_objs = question_objs.filter(category__category_name__icontains=request.GET.get('category'))

        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)  # Shuffle questions randomly
        
        for question_obj in question_objs:
            data.append({
                "uid": question_obj.uid,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "category": question_obj.category.category_name,
                "Answer": question_obj.get_answer()  # Get answers using your model method
            })

        payload = {'status': True, 'data': data}
        return JsonResponse(payload)

    except Exception as e:
        print(e) 
        return HttpResponse("Something went wrong")


# Sidebar
def side_bar(request):
    return render(request, "main/side_bar.html")

# Profile
def profile(request):
    return render(request, "main/profile.html")

# Study Page
def study(request):
    return render(request, "main/study.html")

# Tax Page
def tax(request):
    return render(request, "tax.html")

# Test Category Selection
def test(request):
    context = {'categories': Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/testq/?category={request.GET.get('category')}")
    return render(request, "test.html", context)

# Test Questions Page
def testq(request):
    context = {'category': request.GET.get('category')}
    return render(request, 'testq.html', context)


@csrf_exempt
def submit_answers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        answers = data.get('answers', {})

        total_questions = 0
        correct_answers = 0
        total_marks = 0

        # Loop through the submitted answers and check correctness
        for question_uid, selected_answer in answers.items():
            try:
                question = Question.objects.get(uid=question_uid)
                correct_answer = Answer.objects.filter(question=question, is_correct=True).first()

                total_questions += 1

                if correct_answer and correct_answer.answer == selected_answer:
                    correct_answers += 1
                    total_marks += question.marks  # Increment the marks if the answer is correct
            except Question.DoesNotExist:
                continue

        # Prepare the result
        result = {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'total_marks': total_marks
        }

        return JsonResponse(result)
    return HttpResponse("Invalid request")