from django.urls import path
from . import views
from .views import profile, delete_job_post, verify_job_post, apply_job, dashboard_tracer, delete_tracer, SearchJobsView, recommend_jobs

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    
    path('profile/<int:user_id>/', views.profile, name="profile"),

    path('user-logout/', views.user_logout, name="user-logout"),
    path('company_profile/', views.company_profile, name="company_profile"),
    path('post_job/', views.post_job, name="post_job"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('dashboard_post/', views.dashboard_post, name="dashboard_post"),
    path('dashboard/users/', views.dashboard_users, name='dashboard_users'),
    path('dashboard/users/delete/<str:username>/', views.delete_user, name='delete_user'),

    path('delete_job_post/<int:job_post_id>/', delete_job_post, name='delete_job_post'),
    path('verify_job_post/<int:job_post_id>/', verify_job_post, name='verify_job_post'),
    path('job_find/', views.job_find, name="job_find"),
    path('job_info/<int:job_post_id>', views.job_info, name="job_info"),
    path('apply/<int:job_posting_id>/', apply_job, name='apply_job'),

    path('view_applications/<int:job_post_id>/', views.view_applications, name='view_applications'),

    path('graduate_tracer/', views.graduate_tracer, name="graduate_tracer"),

    path('dashboard_tracer/', dashboard_tracer, name='dashboard_tracer'),
    path('delete_tracer/<str:username>/', delete_tracer, name='delete_tracer'),

    path('search/', SearchJobsView.as_view(), name='search_jobs'),

    path('home/', recommend_jobs, name='home'),  # Adjust the URL pattern accordingly

]
