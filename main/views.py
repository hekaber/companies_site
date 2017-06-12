from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


class LoginView(TemplateView):
    template_name = 'main/index.html'

    def get(self, request, **kwargs):
        form = UserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
        else:
            form = UserCreationForm()
            return render(request, self.template_name, {'form': form})


class LogoutView(TemplateView):
    template_name = 'main/logout.html'

    def get(self, request, **kwargs):
        logout(request)

        return render(request, self.template_name)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('main/welcome.html')
    else:
        form = UserCreationForm()
    return render(request, 'main/index.html', {'form': form})


@login_required
def welcome(request):
    return render(request, 'main/welcome.html')