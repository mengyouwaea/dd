from django.urls import path

from management_system.views import index, add_books, books_list, add_parent_cate, add_child_cate, order_list, all_cate, \
    address, add_books_logic, add_parent_logic, add_chile_cate_logic, del_book

urlpatterns=[
    path('index/',index,name="index"),
    path('add_books/',add_books,name="add_books"),
    path('add_books_logic/',add_books_logic,name="add_books_logic"),

    path('books_list/',books_list,name="books_list"),
    path('del_book/',del_book,name="del_book"),


    path('add_parent_cate/',add_parent_cate,name="add_parent_cate"),
    path('add_parent_logic/',add_parent_logic,name="add_parent_logic"),
    path('add_chile_cate_logic/',add_chile_cate_logic,name="add_chile_cate_logic"),

    path('add_child_cate/',add_child_cate,name="add_child_cate"),
    path('all_cate/',all_cate,name="all_cate"),

    path('address/',address,name="address"),



    path('order_list/',order_list,name="order_list"),
]