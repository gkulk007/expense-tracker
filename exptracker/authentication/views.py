from django.shortcuts import render
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
# Create your views here.


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alpha numeric characters'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Username already exists, please select a new username'})

        return JsonResponse({"username_valid": True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']

        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Email already exists, please use a new email'})

        return JsonResponse({"email_valid": True})


class RegisterationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):

        messages.success(request, "Successfully submitted")
        messages.warning(request, "Successfully submitted warn")
        messages.info(request, "Successfully submitted info")
        messages.error(request, "Successfully submitted error")

        return render(request, 'authentication/register.html')
