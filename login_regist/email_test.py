# 本文件仅供测试邮件的发送练习，跟项目无关

import os
from django.core.mail import send_mail, EmailMultiAlternatives

os.environ['DJANGO_SETTINGS_MODULE'] = 'dd.settings'
if __name__ == '__main__':
    # 第一次简单发送文本文件
    # send_mail(
    # '这是邮件的标题',
    # '简单的小邮件，学习发送！',
    # '17310037026@sina.cn',
    # ['17310037026@163.com'],
    # )
    # 第二次发送html邮件
    subject, from_email, to = '来自的测试邮件', '17310037026@sina.cn', '17310037026@163.com'
    text_content = '欢迎访问www.baidu.com，祝贺你收到了我的邮件，有幸收到我的邮件说明你及其幸运'
    html_content = '<p>感谢注册<a href="http://{}/confirm/?code={}"target = blank > www.baidu.com < / a >，\欢迎你来验证你的邮箱，验证结束你就可以登录了！ < / p > '
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()