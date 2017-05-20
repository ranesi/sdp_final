from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CreateUserForm

def register(request):

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save()
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password1']
            )
            login(request, user)

            return redirect('ta_web:homepage')

        else:

            return render(request, 'registration/register.html', {'form': form})

    else:

        form = CreateUserForm()

        return render(request, 'registration/register.html', {'form': form})


def logout_message(request):

    return render(request, 'ta_web/logout_message.html')
