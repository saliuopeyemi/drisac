from django.urls import path
from . import views


urlpatterns = [
            path("test/", views.Test.as_view(), name="Test-view"),
            path("create-user/",views.CreateNewUserView.as_view(), name="create-new-user"),
            path("user/",views.UserRetrieveView.as_view(),name="retrieve-user"),
            path("login/",views.LoginView.as_view(), name="login"),
            path("delete-user/", views.DeleteUserView.as_view(),name="delete-user"),
            path("all-users/",views.AllUsers.as_view(),name="all-users"),

            path("product/",views.ProductView.as_view(),name="Products"),
            path("product/update/<int:id>/",views.UpdateProductView.as_view(),name="Update-Product"),

            path("expenditure/",views.ExpenditureView.as_view(),name="Expenditure"),
            path("sale/",views.SaleView.as_view(),name="Sale"),
            path("revenue/",views.TotalRevenueView.as_view(),name="Revenue"),
        ]


