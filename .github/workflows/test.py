# from events_mailer import send_mail
# from events_mailer import sbj, gdt
# from datetime import datetime

# recipients: dict = {
#     # 'naan.mxco@gmail.com' : 'Naan-MxCo BeeTee',
#     # 'bayodenancy111@gmail.com' : 'Bolanle Nancy',
#     # 'toniiabudu@gmail.com' : 'Tonii Abudu',
#     'auralex99@gmail.com' : 'Tee',
# }

# print(datetime.now())
# today = gdt()[4]
# print('-'.join(gdt()[1]))
# day_pocket = f'pocket-{today[2:6]}{today[-2:]}.html'

# def normal() -> None:
#     for recipient_mail, recipient_name in recipients.items():
#         text: str = f"hi, {recipient_name},\nthis is a test!"
#         anchor_link: str = "https://naan-mxco.github.io/pocket/pockets/2024-08/away_camp/test.html"
#         send_mail(recipient_mail, recipient_name, sbj(recipient_mail), text, anchor_link)

# def scheduled() -> None:
#     pass

import os
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def gdt():
    #get datetime
    day = {0 : "MN", 1 : "TU", 2 : "WN", 3 : "TR", 4 : "FR", 5 : "SR", 6 : "SN", }
    dayof_week = day[datetime.now().weekday()]
    str_dt= str(datetime.now())[:-10].split(sep=' ')
    now_date = str_dt[0].split('-')
    now_time = str_dt[1].split(':')
    t_date = f"{dayof_week}{now_date[2]}{now_date[1]}-AD{now_date[0]}"
    t_datetime = f"{dayof_week}{now_date[2]}{now_date[1]}-AD{now_date[0]}:{now_time[0]}{now_time[1]}"

    return (dayof_week, now_date, now_time, t_datetime, t_date)

def ordinal_suffix(number):
    n = ''
    uniq = {'1':'st',
            '2':'nd',
            '3':'rd',}
    
    if number <= 0:
        pass
    elif len(str(number)) > 1 and str(number)[-2] == '1':
        n = f'{number}th'
    elif str(number)[-1] in uniq:
        n = f'{number}{uniq[str(number)[-1]]}'
    else:
        n = f'{number}th'
    
    return n

def from419():
    # Define the start date
    start_date = datetime(2024, 4, 19)
    
    # Get the current date
    current_date = datetime.now()
    
    # Calculate the difference between the current date and the start date
    difference = current_date - start_date
    
    # Calculate the number of weeks, months, and years
    weeks = difference.days // 7
    months = difference.days // 30
    years = difference.days // 365

    print(weeks, months, years)
    
    return weeks, months, years



def sbj(recipient_mail):
    #time since 419
    weeks, months, years = from419()
    #subject
    dayof_week, now_date, now_time, t_datetime, t_date = gdt()
    events = {
        'bola' : {
            "condition": now_date[1:] == ['08', '04'],
            "subject": "HAPPY BIRTHDAY, BOLANLE" if recipient_mail == 'bayodenancy111@gmail.com' else "BOLA'S BIRTHDAY"
            },
        'tonii' : {
            "condition": now_date[1:] == ['10', '09'],
            "subject": "TONII'S BIRTHDAY"
            },
        'anno' : {
            "condition": now_date[1:] == ['04', '19'],
            "subject": f"OUR {ordinal_suffix(years)} ANNIVERSARY"
            },
        'mese' : {
            "condition": now_date[2] == '19',
            "subject": f"OUR {ordinal_suffix(months)} MESEVERSARY"
            },
        'week' : {
            "condition": dayof_week == 'FR',
            "subject": f"OUR {ordinal_suffix(weeks)} WEEK-VERSARY"
            },
        'gf' : {
            "condition": now_date[1:] == ['08', '01'],
            "subject": "GIRLFRIENDS' DAY"
        },
    }

    msg_subject = "IT'S "
    for details in events.values():
        if details["condition"]:
            if recipient_mail == 'bayodenancy111@gmail.com' and details["subject"] == "HAPPY BIRTHDAY, BOLANLE!!!":
                return details["subject"]
            elif msg_subject != "IT'S ":
                msg_subject += " AND "
            msg_subject += details["subject"]
    if msg_subject == "IT'S ":
        msg_subject = "check your pocket"
    msg_subject += "!"

    return msg_subject

print(sbj('Tee'))