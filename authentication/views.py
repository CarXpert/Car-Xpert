from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Hard-coded admin credentials check
        if username == 'admin' and password == 'admin123':
            # Check if the 'admin' user exists in the database
            admin_user, created = User.objects.get_or_create(
                username='admin',
                defaults={'is_superuser': True, 'is_staff': True}
            )

            # Set password if user is created
            if created:
                admin_user.set_password('admin123')
                admin_user.save()

            # Log in the admin user
            login(request, admin_user)
            return redirect('main:show_main')

        # Otherwise, proceed with normal authentication
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('main:show_main')  # Redirect to main page after login
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password != password_confirm:
            messages.error(request, 'Passwords do not match!')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            login(request, user)
            return redirect('main:show_main')

    return render(request, 'signup.html')  # Adjusted template path

def logout_view(request):
    # Log the user out
    logout(request)
    # Redirect to the login page after logging out
    return redirect('authentication:login')