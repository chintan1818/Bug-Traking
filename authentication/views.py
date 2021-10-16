from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .forms import SignUpForm
from . import utils


def signin(request):
    if request.method == 'POST':
        username_email = request.POST['username_email']
        password = request.POST['password']

        user = authenticate(username=username_email, password=password)
        if user is None:
            user = authenticate(email=username_email, password=password)

        if user is not None:
            login(request, user)
            return redirect('project:dashboard')
        else:
            messages.error(request, 'Invalid Credentials!')
            return redirect('auth:signin')
    return render(request, 'signin.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            messages.success(
                request, 'Your account is created successfuly! Check your mail inbox to activate your account')
            email_subject = 'Confirm your email @ Bug Tracker'
            email_message = utils.email_template_message(request, user)
            utils.send_email(email_subject, email_message, [user.email])
            return redirect('auth:signin')
    else:
        form = SignUpForm()

    return render(request, template_name='signup.html', context={"form": form})


def activate(request, uidb64, token):
    user, isTokenValid = utils.activateAccount(uidb64, token)

    if user.is_active:
        messages.info(request, 'Your account has already been activated')
        return redirect('auth:signin')
    if user is not None and isTokenValid:
        user.is_active = True
        user.save()
        messages.success(
            request, "Congrats! Your account has been activated. Signin to continue.")
        return redirect('auth:signin')


def signout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully!')
    return redirect('home')
