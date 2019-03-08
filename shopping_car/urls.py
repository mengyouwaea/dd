from django.urls import path

from shopping_car.views import add, modify, remove, show, indent_addr, indent_ok, settlement, auto_addr

urlpatterns=[
    path('show/', show, name="show"),
    path('add/',add,name="add"),
    path('modify/',modify,name="modify"),
    path('remove/',remove,name="remove"),

    path('indent_addr/',indent_addr,name="indent_addr"),
    path('indent_ok/',indent_ok,name="indent_ok"),
    path('settlement/',settlement,name="settlement"),
    path('auto_addr/',auto_addr,name="auto_addr"),


]