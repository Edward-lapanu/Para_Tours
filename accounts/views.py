
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Logout View (Django's built-in)
def logout_view(request):
    return auth_views.LogoutView.as_view()(request)

def login_view(request):
    """Handles the login form"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # If authentication is successful, log the user in
            login(request, user)
            messages.success(request, "You are logged in successfully!")
            
            # Fetch 'next' parameter or fallback to the home page
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)  # Redirect to the original requested page
            else:
                return redirect(reverse('perl_app:index'))  # Redirect to the home page
        else:
            # If authentication fails
            messages.error(request, "Invalid credentials. Please try again.")
    
    # For GET requests, render the login page
    next_url = request.GET.get('next', '')  # Get 'next' parameter, default to empty
    return render(request, 'accounts/login.html', {'next': next_url})

def register_form(request):
    ''' Show the registration form '''
    if request.method == 'POST':
        # Retrieve form data
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')  # Will need additional handling for storage
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password == confirm_password:
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username is already taken.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email is already registered.")
            else:
                # Create user
                try:
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        email=email
                    )
                   
                    user.save()
                    messages.success(request, "Your account has been registered successfully.")
                    return redirect('perl_app:index')  # Redirect to homepage
                except Exception as e:
                    messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Your passwords do not match!")

    return render(request, 'accounts/register.html')




def logout_view(request):
    """Handles logging out the user"""
    logout(request)  # Logs out the user
    messages.success(request, "You have been logged out successfully!")  # Show success message
    return redirect('perl_app:index')  # Redirect to the home page or any other page