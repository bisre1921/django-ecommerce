from django.shortcuts import render , redirect
from .models import Product , Category, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request , 'home.html' , {'products': products})

def about(request):
    return render(request , 'about.html')

def product(request , pk):
    product = Product.objects.get(id=pk)
    return render(request , 'product.html' , {'product': product})

def category_summary(request):
    categories = Category.objects.all()
    return render(request , 'category_summary.html' , {"categories": categories})

def category(request , foo):
    foo = foo.replace('-' , ' ')
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request , 'category.html' , {'products': products , 'category': category})
    except:
        messages.error(request, "Category does not exist")
        return redirect('home')
    

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request , username=username , password=password)
        if user is not None:
            login(request , user)
            messages.success(request, "You are now logged in")
            return redirect('home')
        else:
            messages.success(request, "Invalid credentials, try again")
            return redirect('login')
    else:
        return render(request , 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out")
    return redirect('home')

def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(request, username=username, password=password)
            if user:  # Ensure user is not None
                login(request, user)
                messages.success(request, "Account was created for " + username)
                return redirect('update_user')
            else:
                messages.error(request, "Authentication failed. Please try again.")
                return redirect('register')
        else:
            messages.error(request, "Invalid credentials, try again")
            print(form.errors)
            return redirect('register') 
    else:
        return render(request, 'register.html', {'form': form})

    
def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)

        # Handle POST request
        if request.method == 'POST':
            user_form = UpdateUserForm(request.POST, instance=current_user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "User updated successfully")
                return redirect('home')
        else:
            # Pre-fill form with current user data for GET request
            user_form = UpdateUserForm(instance=current_user)

        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.warning(request, "You must be logged in to update your profile")
        return redirect('login')

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Password updated successfully")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error[0])
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, 'update_password.html', {'form': form})
    else:
        messages.warning(request, "You must be logged in to update your password")
        return redirect('login')

def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user__id=request.user.id)
        except ObjectDoesNotExist:
            messages.error(request, "Profile does not exist for the user.")
            return redirect('home')

        if request.method == 'POST':
            form = UserInfoForm(request.POST, instance=current_user)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Info updated successfully")
                return redirect('home')
        else:
            form = UserInfoForm(instance=current_user)

        return render(request, 'update_info.html', {'form': form})
    else:
        messages.warning(request, "You must be logged in to update your profile")
        return redirect('login')

def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))
        if not searched:
            messages.error(request, "No results found")
            return render(request, 'search.html', {})
        else:
            return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html', {})
