from django.shortcuts import render, redirect
import requests
from django.http import HttpResponse
import json

global notification
global notification_message

notification = False
notification_message = "Success"

api_head = "http://127.0.0.1:8000/api"

def construct_url(endpoint):
    url = f"{api_head}/{endpoint}/"
    return url

def construct_header(token):
    header = {
                "Authorization":f"Bearer {token}"
            }
    return header


def home(request):
    return render(request,"home.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        payload = {
                    "email":email,
                    "password":password
                }
        url = construct_url("login")
        response = requests.post(url,payload)
        if response.status_code == 200:
            data = response.json()
            token = data.get("access")
            response = redirect("dashboard")
            response.set_cookie("token",token,max_age=3600)
            response.set_cookie("notify","Login Success!!")
            return response
        else:
            error = response.json()["error"][0]
            #print(error)
            response = render(request,"home.html",{"error":error})
            return response
    else:
        response = render(request,"home.html",{"error":"You must login first"})
        return response
            

def dashboard(request):
    #global notification_message
    #global notification
    #print(f"Notification:{notification}")
    token = request.COOKIES.get("token")

    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        
        user_url = construct_url("user")

        user = requests.get(user_url,headers=header)
        if user.status_code == 200:
            data = user.json()
        else:
            data = {
	                "email": "Anonymous",
	                "user_type": "user"
                    }

        url = construct_url("product")
        products = requests.get(url,headers=header)

        url = construct_url("all-users")
        all_users = requests.get(url,headers=header)
        all_users = all_users.json()

        expenditure_url = construct_url("expenditure")
        expenditures = requests.get(expenditure_url,headers=header)

        sale_url = construct_url("sale")
        sales = requests.get(sale_url,headers=header)

        if products.status_code == 200:
            products = products.json()
        else:
            products = []
        if expenditures.status_code == 200:
            expenditures = expenditures.json()
        else:
            expenditures = []
        if sales.status_code == 200:
            sales = sales.json()
        else:
            sales = []
        notification = request.COOKIES.get("notify")
        analysis = request.COOKIES.get("analysis","none")
        error = request.COOKIES.get("error")
        if analysis != "none":
            analysis = json.loads(analysis)
        if not notification:
            response = render(request,"dashboard.html",{"products":products,"data":data,"expenditures":expenditures,"sales":sales,"analysis":analysis,"all_users":all_users,"error":error})
            response.delete_cookie("analysis")
            response.delete_cookie("error")
        else:
            response = render(request,"dashboard.html",{"products":products,"data":data,"expenditures":expenditures,"sales":sales,"success":notification,"analysis":analysis,"all_users":all_users,"error":error})
            response.delete_cookie("notify")
            response.delete_cookie("analysis")
            response.delete_cookie("error")

        #print(analysis)
        return response

def add_product(request):
    token =request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        if request.method == "POST":
            header = construct_header(token)
            product_url = construct_url("product")
            title = request.POST.get("title")
            description = request.POST.get("description")
            unit_price = request.POST.get("unit_price")
            payload = {
                        "title":title,
                        "description":description,
                        "unit_price":unit_price
                    }
            response = requests.post(product_url,payload,headers=header)
            if response.status_code == 201:
                #notification = True
                #notification_message = "Product Added Successfully!!"
                response = redirect("dashboard")
                response.set_cookie("notify","Product added successfully.")
                return response
            else:
                response = redirect("dashboard")
                response.set_cookie("error","Unable to add Product.")
                return response

def delete_product(request):
    token = request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("product")
        query_parameter = request.POST.get("product")
        url = f"{url}?product_id={query_parameter}"
        response = requests.delete(url,headers=header)
        if response.status_code == 204:
            response = redirect("dashboard")
            response.set_cookie("notify","Product deleted Successfully!")
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error","Product deletion failed!.")
            return response

def update_product(request):
    token = request.COOKIES.get("token")
    if not token:
        redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("product/update")
        product_id = request.POST.get("product")
        unit_price = request.POST.get("unit_price")
        payload = {
                    "unit_price":unit_price
                }
        response = requests.put(f"{url}{product_id}/",payload,headers=header)
        if response.status_code == 202:
            response = redirect("dashboard")
            response.set_cookie("notify","Product data has been updated!")
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error","Error occurred while updating data!")
            return response



def add_expense(request):
    global notification
    token = request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("expenditure")
        title = request.POST.get("title")
        description = request.POST.get("description")
        amount = request.POST.get("amount")
        payload = {
                    "title":title,
                    "description":description,
                    "amount":amount
                }
        response = requests.post(url,payload,headers=header)
        if response.status_code == 201:
            response = redirect("dashboard")
            response.set_cookie("notify","Expense Added Successfully!")
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error","Error occurred while adding expense!")
            return response


def remove_expense(request):
    token = request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("expenditure")
        param = request.POST.get("expense")
        url = f"{url}?expenditure_id={param}"
        response = requests.delete(url,headers=header)
        if response.status_code == 204:
            response = redirect("dashboard")
            response.set_cookie("notify","Expense removed successfully!!")
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error","Expense not removed!!")
            return response


def add_sale(request):
    token = request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("sale")
        product = request.POST.get("product")
        quantity = request.POST.get("quantity")
        payload = {
                    "product":product,
                    "quantity":quantity
                }
        #print(payload)
        response = requests.post(url,payload,headers=header)
        if response.status_code == 201:
            response = redirect("dashboard")
            response.set_cookie("notify","Sales Record Added!")
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error","Add sales record failed!!")
            return response


def remove_sale(request):
    token = request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("sale")
        param = request.POST.get("sale")
        url = f"{url}?sale_id={param}"
        response = requests.delete(url,headers=header)
        if response.status_code == 204:
            response = redirect("dashboard")
            response.set_cookie('notify',"Record has been deleted!!")
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error","Error occurred while deleting record")
            return response


def analyze(request):
    token = request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("revenue")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        payload = {
                    "from_date":start_date,
                    "to_date":end_date
                }
        response = requests.post(url,payload,headers=header)
        if response.status_code == 200:
            analysis = response.json()
            #print(type(analysis))
            response = redirect("dashboard")
            response.set_cookie("analysis",json.dumps(analysis))
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error","Analysis Failed!!")
            return response



def create_user(request):
    token = request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("create-user")
        email = request.POST.get("email")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        password = request.POST.get("password")
        user_type = request.POST.get("user_type")
        payload = {
                    "email":email,
                    "first_name":first_name,
                    "last_name":last_name,
                    "password":password,
                    "password2":password,
                    "user_type":user_type
                }
        response = requests.post(url,payload,headers=header)
        if response.status_code == 201:
            response = redirect("dashboard")
            response.set_cookie("notify",f"Added {email} as {user_type}")
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error",f"Creating {user_type} for {email} failed!!")
            return response



def delete_user(request):
    token = request.COOKIES.get("token")
    if not token:
        return redirect("login")
    else:
        header = construct_header(token)
        url = construct_url("delete-user")
        user_id = request.POST.get("delete_user")
        payload = {
                    "user_id":user_id
                }
        response = requests.post(url,payload,headers=header)
        if response.status_code == 204:
            response = redirect("dashboard")
            response.set_cookie('notify',f"User has been deleted!!")
            return response
        else:
            response = redirect("dashboard")
            response.set_cookie("error","User deletion failed!")
            return response



def logout(request):
    token = request.COOKIES.get("token")
    response = redirect("home")
    if token:
        response.delete_cookie("token")
    return response
