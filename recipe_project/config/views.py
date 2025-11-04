"""
Authentication Views Module

This module contains view functions for user authentication including
login, logout, and signup functionality. Uses Django's built-in
authentication system.

Views:
    login_view: Handles user login with username/password
    logout_view: Handles user logout and shows success message
    signup_view: Handles new user registration

Dependencies:
    - Django authentication system (django.contrib.auth)
    - AuthenticationForm: Form for login
    - UserCreationForm: Form for user registration
"""

from django.shortcuts import render, redirect  
# Django authentication libraries for login, logout, and user verification
from django.contrib.auth import authenticate, login, logout
# Django built-in forms for authentication (login) and registration (signup)
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
# Django User model (not directly used but imported for reference)
from django.contrib.auth.models import User    


def login_view(request):
    """
    Handle user login with username and password authentication.
    
    This view displays a login form and processes login submissions.
    On successful authentication, users are redirected to the recipe list.
    On failure, an error message is displayed.
    
    Process Flow:
    1. GET request: Display empty login form
    2. POST request: Validate credentials
    3. If valid: Authenticate user and redirect to recipes
    4. If invalid: Show error message and form again
    
    Args:
        request: HttpRequest object containing metadata about the request
    
    Returns:
        HttpResponse: Rendered login template with form and error message
        HttpResponseRedirect: Redirect to recipes list on successful login
    
    Template:
        auth/login.html
    
    Context:
        - form: AuthenticationForm instance with username/password fields
        - error_message: Error text if login fails (None if no error)
    
    Example Flow:
        User visits /login/ → sees login form → enters credentials →
        submits form → if valid, redirected to /recipes/ → if invalid, sees error
    """
    # Initialize error_message to None (no error initially)
    # Will be set to error text if authentication fails
    error_message = None   
    
    # Create an empty authentication form with username and password fields
    # This form is displayed on GET requests
    form = AuthenticationForm()                            

    # Check if this is a POST request (user submitted the login form)
    # When user hits "login" button, POST request is generated
    if request.method == 'POST':       
        # Create form instance with submitted POST data
        # This populates form fields with user's input
        form = AuthenticationForm(data=request.POST)

        # Validate the form (checks required fields, data types, etc.)
        if form.is_valid():                                
            # Extract cleaned data from validated form
            # cleaned_data is sanitized and validated input
            username = form.cleaned_data.get('username')  # Get entered username
            password = form.cleaned_data.get('password')  # Get entered password

            # Use Django's authenticate function to verify credentials
            # Returns User object if valid, None if invalid
            user = authenticate(username=username, password=password)
            
            # Check if authentication was successful
            if user is not None:  # User exists and password is correct
                # Log the user in (creates session)
                # This sets cookies and session data for the user
                login(request, user)                
                # Redirect authenticated user to recipes list page
                # Uses named URL pattern 'recipe:recipes-list'
                return redirect('recipe:recipes-list')
        else:  # Form validation failed or authentication failed
            # Set error message to display to user
            error_message = 'Invalid username or password'

    # Prepare context data to pass to template
    # Context is a dictionary of variables available in the template
    context = {
        'form': form,  # AuthenticationForm instance (empty or with errors)
        'error_message': error_message  # Error text or None
    }
    
    # Render the login template with context data
    # Returns HTML response with login form
    return render(request, 'auth/login.html', context)


def logout_view(request):
    """
    Handle user logout and display success message.
    
    This view logs out the current user by ending their session
    and displays a success page confirming logout.
    
    Process:
    1. End user's session (remove authentication cookies)
    2. Display success page with logout confirmation
    
    Args:
        request: HttpRequest object containing user session data
    
    Returns:
        HttpResponse: Rendered success template
    
    Template:
        auth/success.html
    
    Example Flow:
        User clicks logout → session ended → success page shown
    
    Notes:
        - Can be accessed via GET request (link/button click)
        - Destroys user's session data
        - Does not require login (can't logout if not logged in)
    """
    # Use Django's built-in logout function
    # Removes user's session data and authentication cookies
    logout(request)
    
    # Display success page confirming logout
    # Template shows "Successfully logged out" message
    return render(request, 'auth/success.html')


def signup_view(request):
    """
    Handle new user registration (signup).
    
    This view displays a registration form and processes signup submissions.
    On successful registration, the user is automatically logged in and
    redirected to the recipe list.
    
    Process Flow:
    1. GET request: Display empty signup form
    2. POST request: Validate registration data
    3. If valid: Create user, auto-login, redirect to recipes
    4. If invalid: Show error message and form with errors
    
    Args:
        request: HttpRequest object containing metadata about the request
    
    Returns:
        HttpResponse: Rendered signup template with form and error message
        HttpResponseRedirect: Redirect to recipes list on successful signup
    
    Template:
        auth/signup.html
    
    Context:
        - form: UserCreationForm instance with username/password1/password2 fields
        - error_message: Error text if signup fails (None if no error)
    
    Form Fields:
        - username: Desired username (must be unique)
        - password1: Password (must meet Django's password validators)
        - password2: Password confirmation (must match password1)
    
    Example Flow:
        User visits /signup/ → sees registration form → enters details →
        submits form → if valid, account created and logged in → redirected to /recipes/
        → if invalid, sees error messages
    """
    # Initialize error_message to None (no error initially)
    error_message = None
    
    # Create an empty UserCreationForm
    # This form has username, password1, and password2 fields
    form = UserCreationForm()
    
    # Check if this is a POST request (user submitted the signup form)
    if request.method == 'POST':
        # Create form instance with submitted POST data
        # Populates form with user's registration information
        form = UserCreationForm(data=request.POST)
        
        # Validate the form
        # Checks: username unique, passwords match, password strength
        if form.is_valid():
            # Create the new user account in the database
            # form.save() creates User object and hashes password
            user = form.save()
            
            # Automatically log the user in after successful registration
            # Creates session so user doesn't need to login again
            login(request, user)
            
            # Redirect newly registered user to recipes list page
            # User can immediately start using the app
            return redirect('recipe:recipes-list')
        else:
            # Form validation failed (username taken, passwords don't match, etc.)
            # Set generic error message
            # Specific field errors are available in form.errors
            error_message = 'Please correct the errors below'
    
    # Prepare context data to pass to template
    context = {
        'form': form,  # UserCreationForm instance (empty or with errors)
        'error_message': error_message  # General error message or None
    }
    
    # Render the signup template with context data
    # Returns HTML response with registration form
    return render(request, 'auth/signup.html', context)
