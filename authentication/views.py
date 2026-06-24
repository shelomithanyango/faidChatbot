import re
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import UserProfile


# Centralized blocked domains list
BLOCKED_DOMAINS = [
    'mailinator.com',
    'tempmail.com',
    '10minutemail.com',
    'yopmail.com',
    'sharklasers.com',
    'guerrillamailblock.com',
    'example.com',
    'test.com',
    'fake.com',
    'gmail.con',
    'gnail.com'
]


def signup_view(request):
    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()
        username = request.POST.get("username", "").strip()
        phone_number = request.POST.get("phone_number", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Normalize phone number
        phone_number = phone_number.replace(" ", "")

        if phone_number.startswith("0"):
            phone_number = "+254" + phone_number[1:]

        elif phone_number.startswith("254"):
            phone_number = "+" + phone_number

        # Passwords must match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "authentication/signup.html")

        # Email format validation
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"

        if not re.match(email_regex, email):
            messages.error(request, "Enter a valid email address.")
            return render(request, "authentication/signup.html")

        # Block disposable emails
        domain = email.split("@")[-1]

        if domain in BLOCKED_DOMAINS:
            messages.error(
                request,
                "Registration using disposable email addresses is not allowed."
            )
            return render(request, "authentication/signup.html")

        # Phone number validation
        phone_regex = r'^\+254\d{9}$'

        if not re.match(phone_regex, phone_number):
            messages.error(
                request,
                "Enter a valid Kenyan phone number."
            )
            return render(request, "authentication/signup.html")

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "authentication/signup.html")

        # Email already exists
        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "An account with this email already exists."
            )
            return render(request, "authentication/signup.html")

        # Phone number already exists
        if UserProfile.objects.filter(phone_number=phone_number).exists():
            messages.error(
                request,
                "An account with this phone number already exists."
            )
            return render(request, "authentication/signup.html")

        # Password strength validation
        try:
            validate_password(password1)

        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)

            return render(request, "authentication/signup.html")

        # Create Django User
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Create Profile
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")

    return render(request, "authentication/signup.html")


def login_view(request):
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect("chat:chat")

        messages.error(
            request,
            "Invalid username or password."
        )

        return render(
            request,
            "authentication/login.html"
        )

    return render(
        request,
        "authentication/login.html"
    )


def logout_view(request):
    logout(request)
    return redirect("homepage:home")