# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a programm that collects the on date data of 12306
I wan't to be home!!!!!

"""
import requests
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr    
def check_sta():
    #get access to the json file
    req = requests.get('https://kyfw.12306.cn/otn/leftTicket/queryZ?leftTicketDTO.train_date=2018-02-21&leftTicketDTO.from_station=ZZF&leftTicketDTO.to_station=IOQ&purpose_codes=ADULT')
    resp = req.json()
    #extract data
    info_G73 = {}
    info_G817 = {}
    info_G279 = {}
    info = resp['data']['result']
    for data in info:
        ticket = data.split('|')
        if ticket[3] == 'G73':
            info_G73 = ticket
        if ticket[3] == 'G817':
            info_G817 = ticket
        if ticket[3] == 'G279':
            info_G279 = ticket
    return info_G73[30], info_G817[30], info_G279[30]

def format_add(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
    
def send_email(ticket_info):
    #sending information
    from_add = 'qq915901486@gmail.com'
    pass_ = 'CPTBTPTP'
    reciever = '915901486@qq.com'
    #message information
    msg = MIMEText(ticket_info, 'plain', 'utf-8')
    msg['From'] = format_add("Python autosender {}".format(from_add))
    msg['To'] = format_add("Manager {}".format(reciever))
    msg['Subject'] = Header('The ticket status has changed!', 'utf-8').encode()   
    try:

        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.login(from_add, pass_)
        server.sendmail(from_add, reciever, msg.as_string())
        print('Success')
        server.quit()
    except Exception as e:
        print(e)

def main():
    info_G73, info_G817, info_G279 = check_sta()
    info = 'The status of G73 is {}, of G817 is {}, of G279 is {}'.format(info_G73, info_G817, info_G279)
    if not(info_G73 == '无' and info_G817 == '无' and info_G279 == '无'):
        send_email(info)
    print('Run successfully!')
    
    
if __name__ == '__main__':
    main()
