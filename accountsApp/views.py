from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserRegistrationForm
from django import forms


# class AccountsCreateView(CreateView):
#     form_class = UserRegistrationForm
#     template_name = 'registration.html'
#     success_url = reverse_lazy('login')


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'registration.html', {'user_form': user_form})
