from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True, max_length=30,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'name': 'username'}))
    password = forms.CharField(label="Password", required=True, max_length=30,
                               widget=forms.PasswordInput(attrs={
                                   'class': 'form-control',
                                   'name': 'password'}))


def login_view(request):
    template = 'login.html'
    form = LoginForm
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(request, "You have logged in!")
                return redirect(reverse('budget_summary_unit'))
            else:
                messages.warning(request, "Your account is disabled!")
                return redirect('login')
        else:
            messages.warning(request, "The username or password are not valid!")
            return redirect('login')
    context = {'form': form}
    return render(request, template, context)
