import os
from datetime import datetime

def get_datetime():
    day = {0 : "MN", 1 : "TU", 2 : "WN", 3 : "TR", 4 : "FR", 5 : "SR", 6 : "SN", }
    dayof_week = day[datetime.now().weekday()]
    str_dt= str(datetime.now())[:-10].split(sep=' ')
    now_date = str_dt[0].split('-')
    now_time = str_dt[1].split(':')
    t_date = f"{dayof_week}{now_date[2]}{now_date[1]}-AD{now_date[0]}"
    t_datetime = f"{dayof_week}{now_date[2]}{now_date[1]}-AD{now_date[0]}:{now_time[0]}{now_time[1]}"

    return (dayof_week, now_date, now_time, t_datetime, t_date)


def get_subject(recipient_mail):
    #subject
    dayof_week, now_date, now_time, t_datetime, t_date = get_datetime()
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
            "subject": "OUR ANNIVERSARY"
            },
        'mese' : {
            "condition": now_date[2] == '19',
            "subject": "OUR MESEVERSARY"
            },
        'week' : {
            "condition": dayof_week == 'FR',
            "subject": "OUR WEEK-VERSARY"
            },
        'gf' : {
            "condition": now_date[1:] == ['08', '01'],
            "subject": "GIRLFRIENDS' DAY"
        },
    }

    msg_subject = "IT'S "
    for details in events.values():
        if details["condition"]:
            if msg_subject != "IT'S ":
                msg_subject += " AND "
            msg_subject += details["subject"]
    if msg_subject == "IT'S ":
        msg_subject = "check your pocket"
    msg_subject += "!"

    print(msg_subject)

    return msg_subject