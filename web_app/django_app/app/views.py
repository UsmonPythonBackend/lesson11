from django.shortcuts import render, redirect
from django.template.backends import django
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from .forms import UserRegisterForm, LoginForm
import requests
from django.contrib.auth.mixins import LoginRequiredMixin



class HomePageView(View):
    def get(self, request):
        access_token = request.COOKIES['access_token']
        if not access_token:
            return HttpResponseRedirect('login')

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get("http://127.0.0.3:8006/auth/token/verify", headers=headers)
        if response.json()["status_code"] == 200:
            return render(request, 'home.html')

        elif response.json()["status_code"] == 401:
            response = HttpResponseRedirect("/login/")
            response.delete_cookie("access_token")
            return response

        else:
            return HttpResponse("Request Failed")



class RegisterPageView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            url = 'http://127.0.0.3:8006/auth/register'
            data = {
                "username": username,
                "email": email,
                "password": password
            }
            response = requests.post(url, json=data)
            if response.status_code == 200:
                return HttpResponse("User registered successfully!")
            else:
                return HttpResponse(f"Error: {response.json()['detail']}")
        else:
            form = UserRegisterForm()
            return render(request, 'register.html', {'form': form})


class LoginPageView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            url = "http://127.0.0.3:8006/auth/login"
            data = {
                "username_or_email": form.cleaned_data['username'],
                "password": form.cleaned_data['password']
            }
            response = requests.post(url, json=data)

            if response.json()["status_code"] == 200:
                access_token = response.json()["access_token"]
                response = redirect("home")
                response.set_cookie("access_token", access_token, httponly=True)
                return response
            else:
                HttpResponse(f"Error: {response.json()['detail']}")

        return render(request, 'login.html')


class UsersPageView(View):
    def get(self, request):
        access_token = request.COOKIES['access_token']
        if not access_token:
            return HttpResponseRedirect('login')

        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get("http://127.0.0.3:8006/auth/token/verify", headers=headers)
        if response.json()["status_code"] == 200:
            users = requests.get(f"http://127.0.0.2:8002/auth/users", headers=headers)
            return render(request, 'users.html', {'users': users})

        elif response.json()["status_code"] == 401:
            response = redirect("login")
            response.delete_cookie("access_token")
            return response

        else:
            return HttpResponse("Request Failed")



class PostGetView(View):
    def get(self, request):
        return render(request, 'post.html')

    def post(self, request):
        caption = request.POST.get('caption')
        image_path = request.POST.get('image_path')

        api_url = 'http://127.0.0.3:8006/posts/create'

        data = {
            "caption": caption,
            "image_path": image_path
        }

        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            return render(request, 'post.html')

        else:
            return django.http.JsonResponse({'error': 'Failed to login user', 'details': response.json()},
                                            status=response.status_code)

    def get(self, request, *args, **kwargs):
        page = requests.get("http://127.0.0.3:8006/posts/?size=2").json()['page']
        pages = requests.get("http://127.0.0.3:8006/posts/?size=2").json()["pages"]

        if page is not None:
            if int(page) <= int(pages):
                data = requests.get(f"http://127.0.0.3:8006/posts/?size=2").json()["items"]
                return render(request, "post.html",
                              context={"posts": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.3:8006/posts/?page={page}&size=2").json()["items"]
            return render(request, "post.html",
                          context={"posts": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "post.html", context={"message": "Not found"})


class CommentGetView(View):
    def get(self, request):
        return render(request, 'comment.html')

    def post(self, request):
        content = request.POST.get('content')

        api_url = 'http://127.0.0.1:8001/comments/create'

        data = {
            "content": content,
        }

        response = requests.post(api_url, json=data)
        if response.status_code == 200:
            return render(request, 'comment.html')

        else:
            return django.http.JsonResponse({'error': 'Failed to login user', 'details': response.json()},
                                            status=response.status_code)

    def get(self, request, *args, **kwargs):
        page = requests.get(f"http://127.0.0.3:8006/comments/?size=1").json()['page']
        pages = requests.get(f"http://127.0.0.3:8006/comments/?size=1").json()["pages"]

        if page is not None:
            if int(page) <= int(pages):
                data = requests.get(f"http://127.0.0.3:8006/comments/?size=1").json()["items"]
                return render(request, "comment.html",
                              context={"comments": data, "pages": pages, "page": 1, "next": 2, "previous": 0})

            data = requests.get(f"http://127.0.0.3:8006/comments/?page={page}&size=1").json()["items"]
            return render(request, "comment.html",
                          context={"comments": data, "pages": pages, "page": page, "next": int(page) + 1,
                                   "previous": int(page) - 1})

        return render(request, "comment.html", context={"message": "Not found"})
