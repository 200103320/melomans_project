from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from main.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm, AudioForm

from .models import Song


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"


def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('/index')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'registration/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('/index')


def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect('/index')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect('/index')
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'registration/login.html', context)


def player(request):
    paginator = Paginator(Song.objects.all(), 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "player.html", context)


def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                "email": request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(

            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )

    context['account_form'] = form

    return render(request, "registration/account.html", context)


def index(request):
    ctx = {}
    return render(request, 'index.html', ctx)


def premium(request):
    ctx = {}
    return render(request, 'premium.html', ctx)


def download(request):
    ctx = {}
    return render(request, 'download.html', ctx)


def help(request):
    ctx = {}
    return render(request, 'help.html', ctx)


def songadd(request):
    context = {}
    if request.POST:
        form = AudioForm(request.POST, request.FILES or None)
        if form.is_valid():
            form.save()
            return redirect('/player')
    else:
        form = AudioForm()
    context['form'] = form
    return render(request, 'registration/songadd.html', context)


class SearchResultsView(ListView):
    model = Song
    template_name = 'search_venues.html'

    def get_queryset(self):  # new
        query = self.request.GET.get("q")
        object_list = Song.objects.filter(
            Q(title__icontains=query) | Q(artist__icontains=query)
        )
        return object_list
