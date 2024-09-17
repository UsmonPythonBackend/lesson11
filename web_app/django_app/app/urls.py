from django.urls import path, include
from .views import UsersPageView, PostGetView, CommentGetView, RegisterPageView, LoginPageView, HomePageView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('users/', UsersPageView.as_view(), name='users'),
    path('post/', PostGetView.as_view(), name='post'),
    path('comment/', CommentGetView.as_view(), name='comment'),
    path('login/', LoginPageView.as_view(), name='login'),
    path('register/', RegisterPageView.as_view(), name='register'),
]
