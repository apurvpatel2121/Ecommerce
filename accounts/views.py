from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from accounts.forms import RegisterForm, add_css_class
from accounts.models import Account
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login as login_auth, logout as logout_auth
from django.contrib.auth import authenticate
from django.contrib import messages


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.


def redirect_authenticated_user(register_func):
    def wrapper(request, *args, **kwargs):
        # Add some behavior before the register function is called
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return register_func(request, *args, **kwargs)
    return wrapper


# def send_email(template):


@redirect_authenticated_user
def register(request):
    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, password=password, username=username)
            user.phone_number = phone_number
            user.save()

            # USER_ACTIVATION
            currunt_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': currunt_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            print(message)
            # send_email.send()
            # messages.success(request,"Account created successfully. Email has been sent to your email address please verify your account to activate.")
            return redirect('/accounts/login/?command=verification&email='+email)

    add_css_class(form, 'form-control')
    context = {'form': form}
    return render(request, "accounts/register.html", context)


@redirect_authenticated_user
def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login_auth(request, user)
            messages.success(request, "Login Succesful")
            return redirect("/")
        else:
            messages.error(request, "Please check email and password!")
    return render(request, 'accounts/login.html')


@login_required(login_url="login")
def logout(request):
    logout_auth(request)
    messages.success(request, "You are logged out.")
    return redirect("login")


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank you! your account is now activated.")
        return redirect("login")
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')


def dashboard(request):
    return render(request, 'accounts/dashboard.html', context={})


def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']

        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            # reset password email
            currunt_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': currunt_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            print(message)
            # send_email.send()

            messages.success(
                request, "Password reset email has been sent to your email address.")
            return redirect("login")
        else:
            messages.error(request, "Account does not exists.")
            return redirect("forgot_password")
    return render(request, 'accounts/forgot_password.html', context={
        "reset": False
    })


def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account.objects.get(pk=uid)
    except:
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, "Please reset your password.")
        return redirect("reset_password")
    else:
        messages.error(request, 'Invalid reset link')
        return redirect('login')


def reset_password(request):

    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get("uid")
            user = Account.objects.get(pk=uid)
            user.set_password(confirm_password)
            user.save()
            messages.success(request,"Password has been reset please login!")
            return redirect("login")
        else:
            messages.error(request,"Password does not match!")
    return render(request,"accounts/forgot_password.html",context={
        "reset": True
    })