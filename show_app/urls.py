from django.urls import path

from show_app.views import index_show, book_details_page, booklist_page

urlpatterns=[
    path("index_show/",index_show,name="index_show"),
    path("book_details_page/",book_details_page,name="book_details_page"),
    path("booklist_page/",booklist_page,name="booklist_page"),
]