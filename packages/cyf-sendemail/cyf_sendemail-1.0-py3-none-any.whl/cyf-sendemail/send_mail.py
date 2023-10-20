# -*- coding:utf-8 -*-
# 发送邮箱的加载模块
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import datetime

def send_email(list_all,subject,who_send,who_get):
    mail_sender = "564934850@qq.com"                                  # 发送者邮箱名
    mail_license = 'jymalxvbwyakbcdi'                                 # 发送者邮箱授权码，即开启POP3/SMTP服务获取的token，需替换成你的邮箱
    mail_host = "smtp.qq.com"                                         # SMTP服务器,这里为qq邮箱，若为163邮箱请用163替换qq
    mail_receivers = ["564934850@qq.com"]                             # 收件人邮箱
    mail = MIMEMultipart('related')                                   # 设置邮件主体
    mail["From"] = who_send+"<564934850@qq.com>"                      # 设置发送者邮箱
    mail["To"] = who_get+"<564934850@qq.com>"                         # 设置接受者邮箱
    subject_content = subject                                         # 设置邮件主题
    mail["Subject"] = Header(subject_content, 'utf-8')         # 添加邮件主题
    body_content = list_all
    message_text = MIMEText(body_content, "plain", "utf-8")  # 设置正文内容、文本格式、编码方式
    mail.attach(message_text)                                         # 向MIMEMultipart对象中添加文本对象
    smtp = smtplib.SMTP()                                             # 创建SMTP对象
    smtp.connect(mail_host, 25)                                  # 设置发件人邮箱的域名和端口，端口地址为25
    # smtp.set_debuglevel(1)                                          # 打印和SMTP服务器交互的所有信息
    smtp.login(mail_sender, mail_license)                             # 根据邮箱地址和邮箱收起码登录邮箱
    now_time = datetime.datetime.now().strftime('%Y-%m-%d')           # 获取当前时间
    try:
        smtp.sendmail(mail_sender, mail_receivers, mail.as_string())  # 发送邮件，并设置邮件内容格式为str
        print(now_time + '邮件发送成功')
    except:
        print('邮件发送失败')
    smtp.quit()