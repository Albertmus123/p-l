from django.http import BadHeaderError, HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from .models import MyUser
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from jose import JWTError, jwt
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site



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



class CustomLoginView(LoginView):
    template_name = 'login.html'  # Provide your login template
    fields = ["email", "password"]

    def form_valid(self, form):
        response = super().form_valid(form)

        if not self.request.user.is_authenticated:
            return redirect('login')

        return response

    def get_success_url(self):
        return reverse_lazy('dashboard')




# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'password_reset_form.html'
#     email_template_name = 'password_reset_email.html'
#     subject_template_name = 'password_reset_subject.txt'
#     success_url = '/password_reset/done/'

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