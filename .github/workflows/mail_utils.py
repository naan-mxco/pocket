import os
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

base_url = "https://naan-mxco.github.io/pocket/"

recipients: dict = {
    'naan.mxco@gmail.com' : 'Naan-MxCo BeeTee',
    'bayodenancy111@gmail.com' : 'Bolanle Nancy',
    'toniiabudu@gmail.com' : 'Tonii Abudu',
    'auralex99@gmail.com' : 'Anthony A U',
    # 'abudu.m1700302@st.futminna.edu.ng' : 'The Boss'
}





### ======= DATE FUNCTIONS ======= ###

def gdt(fake_now: datetime | None = None):
    #get datetime, if fake_now is provided, overrides system datetime.
    day_map = {0:"MN",1:"TU",2:"WN",3:"TR",4:"FR",5:"SR",6:"SN"}
    now = fake_now or datetime.now()

    dayof_week = day_map[now.weekday()]
    t_date = f"{dayof_week}{now.day:02}{now.month:02}-AD{now.year}"
    t_datetime = f"{t_date}:{now.hour:02}{now.minute:02}"
    
    return (
        dayof_week,
        [str(now.year), f"{now.month:02}", f"{now.day:02}"],
        [str(now.hour), str(now.minute), str(now.second)],
        t_datetime,
        t_date
    )



def ordinal_suffix(number):
    if 10 <= number % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, "th")
    return f"{number}{suffix}"



def from419(fake_now: datetime | None = None):
    #start date
    start_date = datetime(2024, 4, 19)
    #current date
    current_date = fake_now if fake_now else datetime.now()
    #time between start and current
    difference = current_date - start_date
    
    #number of weeks, months, and years
    weeks = difference.days // 7
    months = difference.days // 30
    years = difference.days // 365
    
    return weeks, months, years



def sbj(recipient_mail=None, fake_now: datetime | None = None):
    #time since 419
    weeks, months, years = from419(fake_now)
    #subject
    dayof_week, now_date, now_time, t_datetime, t_date = gdt(fake_now)
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
            "subject": f"OUR {ordinal_suffix(weeks)} WEEKIVERSARY"
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
        'perche' : {
            "condition" : (now_date[1:] == ['12', '16']) or (now_date[1:] == ['12', '17']) or (now_date[1:] == ['12', '18']),
            "subject" : "A CHECK-IN, JUST BECAUSE"
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





### ======= MAIL ======= ###

def send_mail(recipient_mail, recipient_name, subject, html_content, plain_text):
    #mail configuration
    sender_mail = os.getenv('GERV_MAIL')
    password = os.getenv('GERV_PW')

    #mail container
    msg = MIMEMultipart("alternative")
    msg["To"] = recipient_mail
    msg["Subject"] = subject
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    #server connect
    try:
        with SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_mail, password)

            #send mail
            server.sendmail(sender_mail, recipient_mail, msg.as_string())
            print(f"mail sent to {recipient_name} - {recipient_mail}")

        print("---all mails sent---")
        server.quit()

    except Exception as e:
        print("Failed to send emails. Error:", str(e))