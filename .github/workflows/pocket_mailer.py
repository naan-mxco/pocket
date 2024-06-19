import os
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

recipients: dict = {
    'naan.mxco@gmail.com' : 'Bee Tee',
    'bayodenancy111@gmail.com' : 'Bolanle Nancy',
    'toniiabudu@gmail.com' : 'Tonii Abudu',
}

def get_datetime():
    day = {0 : "MN", 1 : "TU", 2 : "WN", 3 : "TR", 4 : "FR", 5 : "SR", 6 : "SN", }
    dayof_week = day[datetime.now().weekday()]
    str_dt= str(datetime.now())[:-10].split(sep=' ')
    now_date = str_dt[0].split('-')
    now_time = str_dt[1].split(':')
    t_date = f"{dayof_week}{now_date[2]}{now_date[1]}-AD{now_date[0]}:{now_time[0]}{now_time[1]}"

    return (t_date, now_date, dayof_week)

def send_mail():
    #mail configuration
    sender_mail = os.getenv('GERV_MAIL')
    password = os.getenv('GERV_PW')

    #server connect
    try:
        with SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_mail, password)

            for recipient_mail, recipient_name in recipients.items():
                #mail container
                msg = MIMEMultipart('alternative')
                #correspondents
                # msg['From'] = sender_mail
                msg['To'] = recipient_mail
                #subject
                t_date, now_date, dayof_week = get_datetime()
                if (now_date[1:]) == ['08', '04']:
                    if recipient_mail == 'bayodenancy111@gmail.com':
                        msg['Subject'] = "HAPPY BIRTHDAY, BOLANLE!"
                    else:
                        msg['Subject'] = "IT'S BOLA'S BIRTHDAY!"
                elif (now_date[1:]) == ['10', '09']:
                    msg['Subject'] = "TONII'S BIRTHDAY!"
                elif (now_date[1:]) == ['04', '19']:
                    msg['Subject'] = "IT'S OUR ANNIVERSARY!"
                elif (now_date[2]) == '19':
                    msg['Subject'] = "IT'S OUR MESEVERSARY!"
                elif (dayof_week == 'FR') and (((now_date[1:]) != ['08', '04']) or ((now_date[1:]) == ['10', '09'])):
                    msg['Subject'] = "IT'S OUR WEEK-VERSARY!"
                else:
                    msg['Subject'] = f"check your pocket!"

                #mail content
                bg_color = '#005959'
                text_color = '#ffffff'
                link_bg = '#000000'
                link_text = '#ffffff'
                anchor_link: str = "https://naan-mxco.github.io/pocket/"
                text: str = f"hi, {recipient_name},\nyou have a new item in your pocket"
                html_template = f'''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>\n{msg['Subject']}\n</title>\n<style>\nbody {{color: {text_color};padding: 10px;}}\ntable {{width: 350px;margin: 0 auto;background-color: {bg_color};color: {text_color};border: 3px solid #000;}}\nth, td {{padding: 5px;width: 75%;text-align: center;}}\nh1, p {{font-family: Garamond, serif;margin: 0;padding: 5px;}}\nsvg {{margin: 10px auto 0; padding: 5px;}}\nlabel {{font-family: monospace;}}\na {{font-family: monospace;font-size: larger;font-weight: bold;width: 90%;margin: 0 auto 10px;padding: 10px 0;display: block;background-color: {link_bg};color: {link_text};text-decoration: none;}}\n</style>\n</head>\n<body>\n<table align="center">\n<tr>\n<th>\n<table style="border: none;width: 90%;background-color: none;">\n<tr>\n<td align="center">\n<svg display="inline" margin="0" width="20" height="20"><polygon points="0,0 20,0 20,15 10,20 0,15" fill="#fff"/></svg>\n<h1>\n{msg['Subject']}\n</h1>\n<label>\n{t_date}\n</label>\n</td>\n</tr>\n</table>\n<hr style="width: 90%;border: 1px solid {text_color};">\n</th>\n</tr>\n<tr>\n<td align="center">\n<table style="border: none;width: 90%;background-color: none;">\n<tr>\n<td align="center">\n<p style="font-size: 20px;">\n{text}\n</p>\n</td>\n</tr>\n</table>\n</td>\n</tr>\n<tr>\n<td align="center">\n<a href="{anchor_link}">\ncheck it\n</a>\n</td>\n</tr>\n</table>\n</body>\n</html>'''
            
                # print(html_template)
                # print(msg['Subject'])
                # print(text)
                #turn  into plain/html MIMEText objects
                part1 = MIMEText(f"{t_date}\n\n{text}\ncheck it at {anchor_link}", 'plain')
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
     send_mail()