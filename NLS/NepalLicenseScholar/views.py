from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from datetime import datetime
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt  # Make sure this import is here
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from datetime import datetime
from django.contrib.auth.models import User
from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator
from django.contrib import messages
from .models import *
import json
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def about(request):
    return render(request, "about.html")

@login_required
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


@login_required(login_url='login')
def dashboard(request):
    return render(request, "dashboard.html")


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

def signup(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return render(request, 'signup.html')

       
        try:
            EmailValidator()(email)
        except ValidationError:
            messages.error(request, "Please provide a valid email address.")
            return render(request, 'signup.html')

       
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        
        if len(pass1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'signup.html')

       
        try:
            my_user = User.objects.create_user(username=uname, email=email, password=pass1)
            my_user.save()
            messages.success(request, "User has been successfully created!")
        except Exception as e:
            messages.error(request, f"An error occurred while creating the user: {str(e)}")
        
    return render(request, 'signup.html')

@login_required
def notice(request):
    return render(request, "notice.html")


def get_quiz(request):
    try:
        question_objs = Question.objects.all()

      
        if request.GET.get('category'):
            category_filter = request.GET.get('category')
            question_objs = question_objs.filter(category__category_name__icontains=category_filter)

        paginator = Paginator(question_objs, 4)  
        page_number = request.GET.get('page', 1) 
        page_obj = paginator.get_page(page_number)

        data = []
        for question_obj in page_obj:
            
            data.append({
                "uid": question_obj.uid,
                "question": question_obj.question,
                "marks": question_obj.marks,
                "category": question_obj.category.category_name,
                "difficulty": question_obj.difficulty,  
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

def side_bar(request):
    return render(request, "main/side_bar.html")

@login_required
def profile(request):
    return render(request, "main/profile.html")

@login_required
def study(request):
    return render(request, "study.html")

@login_required
def tax(request):
    return render(request, "tax.html")

@login_required
def test(request):
    context = {'categories': Category.objects.all()}
    if request.GET.get('category'):
        return redirect(f"/testq/?category={request.GET.get('category')}")
    return render(request, "test.html", context)


def testq(request):
    context = {'category': request.GET.get('category')}
    return render(request, 'testq.html', context)

def get_next_question(category, difficulty):
    difficulty_map = {
        'Easy': 'Medium',
        'Medium': 'Hard',
        'Hard': 'Medium',  
    }

    questions = Question.objects.filter(category__category_name=category, difficulty=difficulty).order_by('?')

    if questions.exists():
        return questions.first()

    
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
        correct = data.get('correct', True) 

       
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
        total_available_marks = 0 

        
        for question_uid, selected_answer in answers.items():
            try:
                question = Question.objects.get(uid=question_uid)
                correct_answer = Answer.objects.filter(question=question, is_correct=True).first()

                total_questions += 1
                total_available_marks += question.marks  

                if correct_answer and correct_answer.answer == selected_answer:
                    correct_answers += 1
                    total_marks += question.marks  
            except Question.DoesNotExist:
                continue

        
        result = {
            'username': request.user.username,
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'total_marks': total_marks,
            'total_available_marks': total_available_marks  
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

def LogoutPage(request):
    logout(request)
    return redirect('login')