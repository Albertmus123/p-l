from django.http import BadHeaderError, HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from .forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from .models import MyUser
from django.core.mail import send_mail


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
            # Redirect back to the login page with an error message
            return redirect('login')

        return response

    def get_success_url(self):
        return reverse_lazy('dashboard')




class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_url = '/password_reset/done/'

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


