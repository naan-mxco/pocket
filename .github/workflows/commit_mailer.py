from datetime import datetime
from mail_utils import recipients, send_mail, sbj, base_url, gdt, ordinal_suffix



# ======= CONFIG ======= #
DRY_RUN = False  # change to True to enable dry run
FAKE_NOW = None
# FAKE_NOW = datetime(2025, 12, 25, 10, 30)  # ← change freely

anchor_link = base_url
notes_link = base_url + "/notes"





# ======= MAIN ======= #

for email, name in recipients.items():

    subject = sbj(email, fake_now=FAKE_NOW)
    text = f"hi, {name},<br><br>you should check out what's new in your pocket!"

    plain_text = f"""
hi {name},
{text}\n
check your pocket: {anchor_link}
check your notes: {notes_link}
"""

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{subject}</title>
</head>
<body style="padding: 10px; font-family: Garamond, serif;">
<table align="center" style="width: 350px; margin: 2em auto; background-color: #fff; color: #cc383f; border: 1px solid #cc383f; border-radius: 2em">
<tr>
<th>
<table style="border: none;width: 100%;background-color: transparent;padding: 15px 2.5em;">
<tr>
<td align="center">
<img src="https://naan-mxco.github.io/pocket/assets/duoBeeTee.png" alt="Pocket" style="display: inline; margin: 25px auto 0; padding: 5px;" width="auto" height="50px">
<h1 style="margin: 0; padding: 15px; color: #cc383f;">{subject}</h1>
<label style="font-family: monospace; color: #e77291;">{gdt(FAKE_NOW)[3]}</label>
</td>
</tr>
</table>
<hr style="width: 81%; border-color: #cc383f">
</th>
</tr>
<tr>
<td align="center">
<table style="border: none; width: 90%; background-color: transparent;">
<tr>
<td align="center">
<p style="font-size: 1.2em; margin: 0; padding: 0.5em; color: #cc383f">{text}</p>
</td>
</tr>
</table>
</td>
</tr>
<tr>
<td align="center">
<a href="{anchor_link}" style="font-family: monospace; font-size: larger; font-weight: bold; width: 81%; margin: 5px auto; padding: 10px 0; display: block; background-color: #cc383f; border: 1px solid #fff; border-radius: 5em; color: #fff; text-decoration: none;">
check it
</a>
</td>
</tr>
<tr>
<td align="center">
<a href="{notes_link}" style="font-family: monospace; font-size: larger; font-weight: bold; width: 81%; margin: 5px auto; padding: 10px 0; display: block; background-color: #fff; border: 1px solid #cc383f; border-radius: 5em; color: #cc383f; text-decoration: none;">
see all notes
</a>
</td>
</tr>
<tr>
<td align="center" style="width: 100%;padding: .75em 0 1em;"></td>
</tr>
</table>
</body>
</html>"""



    if DRY_RUN:
        print("DRY_RUN=ON")

        # ======= DEBUG ======= #
        print("\n====== DEBUG ======")
        print(f"To: {name} <{email}>")
        print(f"Subject: {subject}")
        print("\n--- PLAIN TEXT ---\n")
        print(plain_text)
        print("\n--- HTML CONTENT ---\n")
        print(html_content)
        print("\n======= END =======\n")
    else:
        print("DRY_RUN=OFF")
        send_mail(
                email,
                name,
                subject,
                html_content,
                plain_text,
            )