from django.http import  HttpResponse, HttpResponseBadRequest
from django.shortcuts import render,redirect
from .forms import UserCreationForm,OTPForm
from django.contrib.auth.decorators import login_required
from .models import MyUser,OTP
from django.core.mail import send_mail
from django.template.loader import render_to_string
from jose import JWTError, jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
import random


sender_of_email = settings.EMAIL_HOST_USER


SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

def create_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "create_account.html", {"form": form})


def login(request):
    if request.method == "POST":
        user_email = request.POST['email']
        user_password = request.POST['password']
        user = authenticate(request,email=user_email, password=user_password)
                
        if user is not None:
            code = random.randint(200000,999999)
            subject = '2 Factor Authentication'
            # Render HTML content from the email template
            html_message = render_to_string('otp_email.html', {
                'code': code,
                'user': user
            })
            send_mail(
                    subject=subject,
                    message='',  # Leave the message empty since you're using HTML
                    from_email=sender_of_email,  # Replace with your email address
                    recipient_list=[user_email],
                    html_message=html_message,
                )
            new_code = OTP.objects.create(code=code,user=user)
            new_code.save()
            return redirect('/otp_page')
         
        else:
            print("credential envalid")
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
 
    return render(request, "login.html")


def otp_render(request):
    if request.method == "POST":
        code = request.POST['code']
        code_veriefy = OTP.objects.get(code=code)
        if code_veriefy is not None:
            user = MyUser.objects.get(email=code_veriefy.user.email)
            login(request,user)
            return redirect('dashboard')
        else:
            return HttpResponseBadRequest('Invalid')

    return render(request, "otp.html")
                




@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

        


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        
        try:
            user = MyUser.objects.get(email=email)
        except MyUser.DoesNotExist:
            return HttpResponse("User doesn't exist")

        data = {'email': user.email}
        token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

        current_site = get_current_site(request)
        subject = 'Reset your Password Account'
        
        # Render HTML content from the email template
        html_message = render_to_string('email.html', {
            'user': user,
            'domain': current_site.domain,
            'token': token,
        })

        # Send the email using send_mail
        send_mail(
            subject=subject,
            message='',  # Leave the message empty since you're using HTML
            from_email=sender_of_email,  # Replace with your email address
            recipient_list=[user.email],
            html_message=html_message,
        )

        return HttpResponse('Your email has been sent')

    return render(request, 'reset_password.html')


def reset_form(request,token):
    if request.method == 'POST':
        new_password = request.POST['password']
        confirm_password = request.POST['password_confirmation']
        
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email: str = payload.get("email")
            if email is None:
                raise HttpResponseBadRequest("Invalid email")
        except JWTError:
            raise HttpResponseBadRequest("Invalid token")
        
        try:
            user = MyUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            return redirect('/login')
        
        except MyUser.DoesNotExist:
            return False  # User not found
        
    return render(request, 'reset_form.html')