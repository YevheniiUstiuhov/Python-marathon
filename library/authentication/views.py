from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse

from .models import CustomUser

from .forms import LoginForm, RegisterForm


# Create your views here.
def home(request):
    return render(request, 'authentication/home.html', {})


def login_user(request):

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user:
                messages.success(request, "You've successfully logged in")
                login(request, user)
                return redirect("home")
            else:
                messages.error(request, "The email or password is incorrect")
                return redirect("login")

    else:
        form = LoginForm()
        return render(request, 'authentication/login.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        middle_name = request.POST.get('middle_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        if role == '0':
            # create a visitor user
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                role=0,
            )
        else:
            # create a librarian user
            user = CustomUser.objects.create_superuser(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                middle_name=middle_name,
                role=1,
            )
        if user:
            messages.success(request, 'Account created successfully')
            return redirect('login')
    else:
        form = RegisterForm()
        return render(request, 'authentication/register.html', {'form': form})


def logout_user(request):
    messages.info(request, 'You sign out')
    logout(request)
    return redirect('home')


@login_required(login_url='login/')
@staff_member_required
def get_users(request):
    users = CustomUser.objects.all()
    context = {'users': users}
    return render(request, 'authentication/user_list.html', context)


@login_required(login_url='login/')
@staff_member_required
def user_detail(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    context = {'user': user}
    return render(request, 'authentication/user_detail.html', context)
