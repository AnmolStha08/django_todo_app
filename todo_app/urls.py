from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path("users/", views.register_view),
    path("logins/", views.login_view),
    path("logouts/",views.logout_view, name='logouts'),
    path("todos/", views.todo_list),
    path("todos/<int:pk>", views.todo_detail),
    # path("token", obtain_auth_token, name='api_token_auth'),
    #  path('users/me', views.get_user_details),
    # path("users/<int:pk>", views.user_change)
]


# urls:
    # http://127.0.01:8000/signups
    # http://127.0.01:8000/signups/id