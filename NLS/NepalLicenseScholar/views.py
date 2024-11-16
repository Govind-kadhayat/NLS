from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Signup
from.models import *
import re
import json
import random
from django.core.paginator import Paginator

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
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

# Registration View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
import re
from .models import Signup



def register(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        # Basic validation checks
        if not name or not email or not password or not phone or not address:
            messages.error(request, "All fields are required.")
            return render(request, "signup.html")

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Enter a valid email address.")
            return render(request, "signup.html")

        # Check if email already exists
        if Signup.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, "signup.html")

        # Validate phone number (should be exactly 10 digits)
        if not re.match(r'^\d{10}$', phone):
            messages.error(request, "Enter a valid 10-digit phone number.")
            return render(request, "signup.html")

        # Validate password length
        if len(password) < 6:
            messages.error(request, "Password must be at least 6 characters long.")
            return render(request, "signup.html")

        # Hash the password
        hashed_password = make_password(password)

        # Save the Signup object to the database
        try:
            signup = Signup(
                name=name,
                email=email,
                password=hashed_password,
                phone=phone,
                address=address,
                date=timezone.now()
            )
            signup.save()
            messages.success(request, "Registration successful!")
            return redirect('login')  # Redirect to login page after successful registration
        except Exception as e:
            print(f"Error while saving user data: {e}")
            messages.error(request, "There was an issue saving your registration data.")
            return render(request, "signup.html")

    return render(request, "signup.html")

# Notice Page
def notice(request):
    return render(request, "notice.html")


def get_quiz(request):
    try:
        question_objs = Question.objects.all()

        # Filter questions based on category if provided
        if request.GET.get('category'):
            category_filter = request.GET.get('category')
            question_objs = question_objs.filter(category__category_name__icontains=category_filter)

        paginator = Paginator(question_objs, 4)  # Show 4 questions per page
        page_number = request.GET.get('page', 1)  # Default to the first page
        page_obj = paginator.get_page(page_number)

        data = []
        for question_obj in page_obj:
            # Adding the difficulty field to the question data
            data.append({
                "uid": question_obj.uid,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "category": question_obj.category.category_name,
                "difficulty": question_obj.difficulty,  # Add difficulty here
                "Answer": question_obj.get_answer()
            })

        payload = {
            'status': True,
            'data': data,
            'has_next': page_obj.has_next(),
            'has_previous': page_obj.has_previous(),
            'current_page': page_obj.number,
            'total_pages': page_obj.paginator.num_pages
        }

        return JsonResponse(payload)

    except Exception as e:
        print(e)
        return JsonResponse({"error": "Something went wrong"}, status=500)
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

def get_next_question(category, difficulty):
    difficulty_map = {
        'Easy': 'Medium',
        'Medium': 'Hard',
        'Hard': 'Medium',  # If the user gets "Hard" wrong, show "Medium" again
    }

    questions = Question.objects.filter(category__category_name=category, difficulty=difficulty).order_by('?')

    if questions.exists():
        return questions.first()

    # If no question is found for the given difficulty, return the next fallback difficulty
    fallback_difficulty = difficulty_map.get(difficulty, 'Easy')
    fallback_questions = Question.objects.filter(category__category_name=category, difficulty=fallback_difficulty).order_by('?')
    return fallback_questions.first() if fallback_questions.exists() else None
@csrf_exempt
def adaptive_question_view(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)

        category = data.get('category', '')
        previous_difficulty = data.get('previous_difficulty', 'Easy')
        correct = data.get('correct', True)  # Assume correct by default for new session

        # Determine next difficulty
        if correct:
            next_difficulty = {
                'Easy': 'Medium',
                'Medium': 'Hard',
                'Hard': 'Hard',
            }.get(previous_difficulty, 'Easy')
        else:
            next_difficulty = {
                'Hard': 'Medium',
                'Medium': 'Easy',
                'Easy': 'Easy',
            }.get(previous_difficulty, 'Easy')

        next_question = get_next_question(category, next_difficulty)

        if next_question:
            return JsonResponse({
                'success': True,
                'question': {
                    'uid': next_question.uid,
                    'question': next_question.question,
                    'difficulty': next_question.difficulty,
                    'answers': list(next_question.answers.values('answer', 'is_correct')),
                }
            })
        else:
            return JsonResponse({'success': False, 'message': 'No more questions available.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})








@login_required
def submit_answers(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        answers = data.get('answers', {})

        total_questions = 0
        correct_answers = 0
        total_marks = 0
        total_available_marks = 0  # Initialize total available marks

        # Loop through the submitted answers and check correctness
        for question_uid, selected_answer in answers.items():
            try:
                question = Question.objects.get(uid=question_uid)
                correct_answer = Answer.objects.filter(question=question, is_correct=True).first()

                total_questions += 1
                total_available_marks += question.marks  # Add to total available marks

                if correct_answer and correct_answer.answer == selected_answer:
                    correct_answers += 1
                    total_marks += question.marks  # Increment the marks if the answer is correct
            except Question.DoesNotExist:
                continue

        # Prepare the result including total available marks
        result = {
            'username': request.user.username,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'total_marks': total_marks,
            'total_available_marks': total_available_marks  # Add total available marks
        }

        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request"}, status=400)
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
            'username': request.user.username,  # Add the username here
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'total_marks': total_marks
        }

        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request"}, status=400)

