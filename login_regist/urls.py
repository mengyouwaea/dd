from django.urls import path

from login_regist.views import regist_view, regist_logic, generate_captcha, verfiy_name, verfiy_email, verfiy_code, \
    regist_ok, login_view, login_logic, verfiy_login, exits, re_code

urlpatterns=[
    path('regist_view/',regist_view,name="regist_view"),
    path('regist_logic/',regist_logic,name="regist_logic"),
    path('regist_ok/',regist_ok,name="regist_ok"),
    path('re_code/',re_code,name="re_code"),

    path('captcha/',generate_captcha,name="captcha"),
    path('verfiy_name/',verfiy_name,name="verfiy_name"),
    path('verfiy_email/',verfiy_email,name="verfiy_email"),
    path('verfiy_code/',verfiy_code,name="verfiy_code"),

    path('login_view/', login_view, name="login_view"),
    path('login_logic/', login_logic, name="login_logic"),
    path('verfiy_login/', verfiy_login, name="verfiy_login"),

    path('exits/', exits, name="exits"),


]