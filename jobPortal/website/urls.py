from django.urls import path
from . import views
from .views import profile

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('user-logout/', views.user_logout, name="user-logout"),
    path('company_profile/', views.company_profile, name="company_profile"),
    path('post_job/', views.post_job, name="post_job"),
]
