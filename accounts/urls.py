from django.contrib import admin
from django.urls import path,include
from .views import home,product,customer,create_order,update_order,delete_order,registerPage,LoginPage,LogoutUser

app_name = "Accounts"

urlpatterns = [
    path("",home,name="home"),
    path("product/",product,name="product"),
    path("register/",registerPage,name="registerPage"),
    path("login/",LoginPage,name="LoginPage"),
    path('LogoutUser/',LogoutUser,name="LogoutUser"),
    path("customer/<int:id>",customer,name="customer"),
    path("createorder/<int:id>",create_order,name="create_order"),
    path("updateorder/<int:id>",update_order,name="update_order"),
    path("deleteorder/<int:id>",delete_order,name="delete_order"),
]
