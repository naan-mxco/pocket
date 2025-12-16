import os
import json
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

base_url = "https://naan-mxco.github.io/pocket/"

recipients: dict = {
    # 'naan.mxco@gmail.com' : 'Naan-MxCo BeeTee',
    # 'bayodenancy111@gmail.com' : 'Bolanle Nancy',
    # 'toniiabudu@gmail.com' : 'Tonii Abudu',
    # 'auralex99@gmail.com' : 'Anthony A U'
    'abudu.m1700302@st.futminna.edu.ng' : 'The Boss'
}





### DATE FUNCTIONS ###

def gdt():
    #get datetime
    day_map = {0:"MN",1:"TU",2:"WN",3:"TR",4:"FR",5:"SR",6:"SN"}
    now = datetime.now()
    dayof_week = day_map[now.weekday()]
    t_date = f"{dayof_week}{now.day:02}{now.month:02}-AD{now.year}"
    t_datetime = f"{t_date}:{now.hour:02}{now.minute:02}"
    return dayof_week, [str(now.year), f"{now.month:02}", f"{now.day:02}"], [str(now.hour), str(now.minute), str(now.second)], t_datetime, t_date



def ordinal_suffix(number):
    if 10 <= number % 100 <= 20:
        return f"{number}th"
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, "th")



def from419():
    #start date
    start_date = datetime(2024, 4, 19)
    #current date
    current_date = datetime.now()
    #time between start and current
    difference = current_date - start_date
    
    #number of weeks, months, and years
    weeks = difference.days // 7
    months = difference.days // 30
    years = difference.days // 365
    
    return weeks, months, years



def sbj(recipient_mail):
    #time since 419
    weeks, months, years = from419()
    #subject
    dayof_week, now_date, now_time, t_datetime, t_date = gdt()
    events = {
        'bola' : {
            "condition": now_date[1:] == ['08', '04'], #month, day
            "subject": "HAPPY BIRTHDAY, BOLANLE" if recipient_mail == 'bayodenancy111@gmail.com' else "BOLA'S BIRTHDAY"
            },
        'tonii' : {
            "condition": now_date[1:] == ['10', '09'],
            "subject": "OUR BIRTHDAY"
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
        'sun' : {
            "condition": now_date[1:] == ['11', '10'],
            "subject": "THE DAY TEE KISSED THE SUN"
        },
        'xmas' : {
            "condition": now_date[1:] == ['12', '25'],
            "subject": "CHRISTMAS"
        },
        'xmasszn': {
            "condition": (now_date[1] == '12' and int(now_date[2]) >= 26) or (now_date[1] == '01' and int(now_date[2]) <= 6),
            "subject": (
                            f"CHRISTMAS SEASON (Day {int(now_date[2]) - 24}/12)" if now_date[1] == '12' else
                            f"CHRISTMAS SEASON (Day {int(now_date[2]) + 7}/12)" if int(now_date[2]) <= 5 else
                            "EPIPHANY / THREE KINGS' DAY"
                        )
        },
        'newyr' : {
            "condition": now_date[1:] == ['01', '01'],
            "subject": "NEW YEAR"
        },
        'vals' : {
            "condition": now_date[1:] == ['02', '14'],
            "subject": "VALENTINE'S DAY"
        },
        'iwd' : {
            "condition": now_date[1:] == ['03', '08'],
            "subject": "INTERNATIONAL WOMEN'S DAY"
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





### MAIL ###
def send_mail(recipient_mail, recipient_name, subject, text, anchor_link):
    #mail configuration
    sender_mail = os.getenv('GERV_MAIL')
    password = os.getenv('GERV_PW')
    t_datetime = gdt()[3]

    #server connect
    try:
        with SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_mail, password)

            
            #mail container
            msg = MIMEMultipart('alternative')
            #correspondents
            # msg['From'] = sender_mail
            msg['To'] = recipient_mail
            msg['Subject'] = subject
            #mail body
            bg_color = '#005959'
            text_color = '#ffffff'
            link_bg = '#000000'
            link_text = '#ffffff'
            #mail contents
            anchor_link: str = "https://naan-mxco.github.io/pocket/"
            notes_link: str = "https://naan-mxco.github.io/pocket/notes.html"
            html_template = f'''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{msg['Subject']}</title>\n</head>\n<body style="padding: 10px; font-family: Garamond, serif;">\n<table align="center" style="width: 350px; margin: 2em auto; background-color: #fff; color: #cc383f; border: 1px solid #cc383f; border-radius: 2em">\n<tr>\n<th>\n<table style="border: none;width: 100%;background-color: transparent;padding: 15px 2.5em;">\n<tr>\n<td align="center">\n<img src="https://naan-mxco.github.io/pocket/assets/duoBeeTee.png" alt="Pocket" style="display: inline; margin: 25px auto 0; padding: 5px;" width="auto" height="50px">\n<h1 style="margin: 0; padding: 15px; color: #cc383f;">{msg['Subject']}</h1>\n<label style="font-family: monospace; color: #e77291;">{t_datetime}</label>\n</td>\n</tr>\n</table>\n<hr style="width: 81%; border-color: #cc383f">\n</th>\n</tr>\n<tr>\n<td align="center">\n<table style="border: none; width: 90%; background-color: transparent;">\n<tr>\n<td align="center">\n<p style="font-size: 20px; margin: 0; padding: 1.5em; color: #cc383f">{text}</p>\n</td>\n</tr>\n</table>\n</td>\n</tr>\n<tr>\n<td align="center">\n<a href="{anchor_link}" style="font-family: monospace; font-size: larger; font-weight: bold; width: 81%; margin: 5px auto; padding: 10px 0; display: block; background-color: #cc383f; border: 1px solid #fff; border-radius: 5em; color: #fff; text-decoration: none;">\ncheck it\n</a>\n</td>\n</tr>\n<tr>\n<td align="center">\n<a href="{notes_link}" style="font-family: monospace; font-size: larger; font-weight: bold; width: 81%; margin: 5px auto; padding: 10px 0; display: block; background-color: #fff; border: 1px solid #cc383f; border-radius: 5em; color: #cc383f; text-decoration: none;">\nsee all notes\n</a>\n</td>\n</tr>\n<tr>\n<td align="center" style="width: 100%;padding: .75em 2.5em;"></td>\n</tr>\n</table>\n</body>\n</html>'''
        
            # print(html_template)
            # print(msg['Subject'])
            # print(text)
            #turn  into plain/html MIMEText objects
            part1 = MIMEText(f"{t_datetime}\n\n{text}\ncheck it at {anchor_link},\see all notes at {notes_link}.", 'plain')
            part2 = MIMEText(html_template, 'html')
            #attach parts into message container
            msg.attach(part1)
            msg.attach(part2)

            #send mail
            server.sendmail(sender_mail, recipient_mail, msg.as_string())
            print(f"mail sent to {recipient_name} - {recipient_mail}")

        print("---all mails sent---")
        server.quit()

    except Exception as e:
        print("Failed to send emails. Error:", str(e))

if __name__ == '__main__':
    for recipient_mail, recipient_name in recipients.items():
        text: str = f"hi, {recipient_name},\nyou should check out what's new in your pocket. love you!"
        anchor_link: str = "https://naan-mxco.github.io/pocket/"
        send_mail(recipient_mail, recipient_name, sbj(recipient_mail), text, anchor_link)