import os
from datetime import datetime
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from events_mailer import gdt

recipients: dict = {
    'naan.mxco@gmail.com' : 'Naan-MxCo BeeTee',
    'bayodenancy111@gmail.com' : 'Bolanle Nancy',
    'toniiabudu@gmail.com' : 'Tonii Abudu',
    'auralex99@gmail.com' : 'Anthony A U'
}

def send_mail(recipient_mail, recipient_name, subject, text, anchor_link):
    #mail configuration
    sender_mail = 'gervanz.ix@gmail.com'
    password = 'oryi kjra deht emlb'
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
            notes_link: str = "https://naan-mxco.github.io/pocket/notes.html"
            html_template = f'''<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{msg['Subject']}</title>\n</head>\n<body style="padding: 10px; font-family: Garamond, serif;">\n<table align="center" style="width: 350px; margin: 2em auto; background-color: #fff; color: #333; border: 1px solid #949494; border-radius: 2em">\n<tr>\n<th>\n<table style="border: none;width: 100%;background-color: transparent;padding: 15px 2.5em;">\n<tr>\n<td align="center">\n<img src="https://naan-mxco.github.io/pocket/assets/pocket-icon-black.png" alt="Pocket" style="display: inline; margin: 0 auto; padding: 5px;" width="20" height="20">\n<h1 style="margin: 0; padding: 15px; color: #333;">{msg['Subject']}</h1>\n<label style="font-family: monospace; color: #333;">{t_datetime}</label>\n</td>\n</tr>\n</table>\n<hr style="width: 81%;">\n</th>\n</tr>\n<tr>\n<td align="center">\n<table style="border: none; width: 90%; background-color: transparent;">\n<tr>\n<td align="center">\n<p style="font-size: 20px; margin: 0; padding: 1.5em;">{text}</p>\n</td>\n</tr>\n</table>\n</td>\n</tr>\n<tr>\n<td align="center">\n<a href="{anchor_link}" style="font-family: monospace; font-size: larger; font-weight: bold; width: 81%; margin: 5px auto; padding: 10px 0; display: block; background-color: #333; border: 1px solid #333; border-radius: 5em; color: #fff; text-decoration: none;">\ncheck\n</a>\n</td>\n</tr>\n<tr>\n<td align="center">\n<a href="{notes_link}" style="font-family: monospace; font-size: larger; font-weight: bold; width: 81%; margin: 5px auto; padding: 10px 0; display: block; background-color: #fff; border: 1px solid #949494; border-radius: 5em; color: #949494; text-decoration: none;">\nsee all notes\n</a>\n</td>\n</tr>\n<tr>\n<td align="center" style="width: 100%;padding: .75em 2.5em;"></td>\n</tr>\n</table>\n</body>\n</html>'''  #\n<tr>\n<td align="center">\n<a href="https://naan-mxco.github.io/pocket/notes/2024-09/note-260924.html" style="font-family: monospace; font-size: larger; font-weight: bold; width: 81%; margin: 5px auto; padding: 10px 0; display: block; background-color: #fff; border: 1px solid #949494; border-radius: 5em; color: #949494; text-decoration: none;">\nsee "Bear with me" (BTR2609-AD2024)\n</a>\n</td>\n</tr>
        
            # print(html_template)
            # print(msg['Subject'])
            # print(text)
            #turn  into plain/html MIMEText objects
            part1 = MIMEText(f"{t_datetime}\n\n{text}\ncheck it at {anchor_link},\nsee all notes at {notes_link}.", 'plain')
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
        subject: str = "your camp notes are ready!"
        text: str = f"hi, {recipient_name},\nyou have not-so-new pocket notes from camp! just a reminder that Company loves Misery and thanks Misery for keeping Company company in camp ❤"
        anchor_link: str = "https://naan-mxco.github.io/pocket/notes/2024-camp/campnote-1.html"
        send_mail(recipient_mail, recipient_name, subject, text, anchor_link)