from django.shortcuts import render, redirect  
# Django authentication libraries
from django.contrib.auth import authenticate, login, logout
# Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User    

# Define a function view called login_view that takes a request from user
def login_view(request):
    # Initialize error_message to None
    error_message = None   
    # Form object with username and password fields
    form = AuthenticationForm()                            

    # When user hits "login" button, then POST request is generated
    if request.method == 'POST':       
        # Read the data sent by the form via POST request
        form = AuthenticationForm(data=request.POST)

        # Check if form is valid
        if form.is_valid():                                
            username = form.cleaned_data.get('username')  # read username
            password = form.cleaned_data.get('password')  # read password

            # Use Django authenticate function to validate the user
            user = authenticate(username=username, password=password)
            if user is not None:  # if user is authenticated
                # Then use pre-defined Django function to login
                login(request, user)                
                # & send the user to desired page (recipes list)
                return redirect('recipe:recipes-list')
        else:  # in case of error
            error_message = 'Invalid username or password'  # print error message

    # Prepare data to send from view to template
    context = {
        'form': form,  # send the form data
        'error_message': error_message  # and the error_message
    }
    # Load the login page using "context" information
    return render(request, 'auth/login.html', context)


# Define a function view called logout_view that takes a request from user
def logout_view(request):
    # Use pre-defined Django function to logout
    logout(request)
    # After logging out go to success page
    return render(request, 'auth/success.html')


# Define a function view called signup_view for user registration
def signup_view(request):
    error_message = None
    form = UserCreationForm()
    
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        
        if form.is_valid():
            # Create the user
            user = form.save()
            # Log the user in automatically after signup
            login(request, user)
            # Redirect to recipes list
            return redirect('recipe:recipes-list')
        else:
            error_message = 'Please correct the errors below'
    
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'auth/signup.html', context)
