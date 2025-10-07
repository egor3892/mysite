from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .forms import LoginForm, UserRegistrationForm
from django.shortcuts import render, redirect
from .models import Post, Department
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django import forms
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

def posts(request):
    posts = Post.objects.all()
    return render(request, "blog/posts.html", {"posts": posts})

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

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
            if user is not None and user.is_active:
                login(request, user)
                # Remember me обработка
                if not request.POST.get('remember'):
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(1209600)
                return redirect('home')
            else:
                return HttpResponse('Invalid login or disabled account')
    else:
        form = LoginForm()
    return render(request, 'blog/loginpage.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponse("You can't edit this post.", status=403)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.body = request.POST.get('body')
        post.save()
        return redirect('posts')
    return render(request, 'blog/edit_post.html', {'post': post})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author != request.user:
        return HttpResponse("You can't delete this post.", status=403)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    return render(request, 'blog/delete_post.html', {'post': post})


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body']

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Привязываем автора
            post.save()
            return redirect('posts')
    else:
        form = PostForm()
    return render(request, 'blog/add_post.html', {'form': form})
