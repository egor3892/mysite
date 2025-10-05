from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm
from django.shortcuts import render, redirect
from .models import Post, Department
# Create your views here.
def home(request):
    postsfiltered = Post.objects.filter(body__regex=r"\d{4}")
    posts = Post.objects.all()
    all_departments = Department.objects.all()
    print(all_departments)

    postsdep = Post.objects.filter(department__title="title2")
    # print(list(workers_macro_data))
    for p in postsdep:
        print(p.title, p.department)
    return render(request, "blog/index.html", { "posts":posts})

def aboutpage(request):
    return render(request, "blog/aboutpage.html", {})

def signupdone(request):
    return render(request, "signupdone.html", {})

def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signupdone')
    else:
        form = UserRegistrationForm()
    return render(request, "blog/signup.html", {"form": form})



def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username=cd['username'],
                password=cd['password']
            )
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse('Authenticated successfully')
            else:
                return HttpResponse('Disabled account')
        else:
            return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'blog/loginpage.html', {'form': form})
