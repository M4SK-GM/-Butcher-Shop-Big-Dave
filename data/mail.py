# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version


def send_mail(toaddr, code):
    server = 'smtp.mail.ru'
    user = 'butchershopbigdave@mail.ru'
    password = 'RgeAyRI11ri_'

    recipients = [toaddr]
    sender = 'butchershopbigdave@mail.ru'
    subject = 'Подтверждение Email на сайте Мясной лавки Большого Дэйва'
    text = f'Хэй, я вижу ты пытаешься зарегистрироваться на сайте Большого Дэйва? Круто! Тогда вот тебе код для подтверждения Email: {code}'
    html = '<html><head></head><body><p>' + text + '</p></body></html>'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = 'Butcher Shop Big Dave <' + sender + '>'
    msg['To'] = ', '.join(recipients)
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, recipients, msg.as_string())
    mail.quit()
