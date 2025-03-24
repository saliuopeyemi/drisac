from django.urls import path
from . import views


urlpatterns = [
            path("test/", views.Test.as_view(), name="Test-view"),
            path("create-user/",views.CreateNewUserView.as_view(), name="create-new-user"),
            path("login/",views.LoginView.as_view(), name="login"),
            path("delete-user/", views.DeleteUserView.as_view(),name="delete-user"),
        ]


