from django.urls import path
from . import views

urlpatterns = [
            path("",views.home,name="home"),
            path("login/",views.login,name="login"),
            path("logout/",views.logout,name="logout"),
            path("dashboard/",views.dashboard,name="dashboard"),
            path("product/add/",views.add_product,name="add-product"),
            path("product/update/",views.update_product,name="update-product"),
            path("product/delete/", views.delete_product,name="delete-product"),
            path("expenditure/add/",views.add_expense,name="add-expense"),
            path("expenditure/remove/",views.remove_expense,name="remove-expense"),
            path("sale/add/",views.add_sale,name="add-sale"),
            path("sale/remove/",views.remove_sale,name="remove-sale"),
            path("analyze/",views.analyze,name="analysis"),
            path("create/user/",views.create_user,name="create-user"),
            path("delete/user/",views.delete_user,name="delete-user"),
        ]
