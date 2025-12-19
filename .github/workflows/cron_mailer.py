import json
from pathlib import Path
from datetime import datetime
from mail_utils import recipients, send_mail, sbj, base_url, gdt, ordinal_suffix



# ======= CONFIG ======= #
DRY_RUN = False  # True for Dry run, False to send
FAKE_NOW = None
# FAKE_NOW = datetime(2025, 12, 19, 10, 30)  # ← change freely

card_template = """
<tr>
<td align="center">
<a href="{link}" style="font-size: larger; width: 81%; display: block; background-color: #cc383f; border: 1px solid #fff; border-radius: 1em; color: #fff; text-decoration: none;">
<p style="font-size: 1.25em; font-weight: bold; margin: 5px auto 0; padding: 10px 12px 0; text-align: left;">{title}</p>
<p style="font-size: 0.85em; margin: 1px auto 5px; padding: 0 12px 10px; text-align: left;">{date}</p>
</a>
</td>
</tr>
"""

# ======= HELPERS ======= #

def load_notes():
    # repo root is two parents up from .github/workflows/<this-file>
    repo_root = Path(__file__).resolve().parents[2]
    notes_file = repo_root / "notes_index.json"
    if not notes_file.exists():
        # either return empty or raise a clearer error
        return []        # or: raise FileNotFoundError(f"{notes_file} not found")
    return json.loads(notes_file.read_text(encoding="utf-8"))

def filter_notes_for_today(notes, fake_now=None):
    _, now_date, _, _, _ = gdt(fake_now)
    today_mmdd = f"{now_date[1]}-{now_date[2]}"
    matched = []
    for note in notes:
        # note["date"] is YYYY-MM-DD
        if note["date"][5:] == today_mmdd:
            matched.append(note)
    return matched

def build_cards(notes):
    return "\n".join(card_template.format(link=n["url"], title=n["title"], date=n["date"]) for n in notes)

def build_dynamic_text(notes, fake_now=None):
    _, now_date, _, _, _ = gdt(fake_now)
    ordinal_day = ordinal_suffix(int(now_date[2]))
    if not notes:
        return f"this is just a reminder that today is another special day; {sbj(fake_now=FAKE_NOW).lower()}"
    return f"this is just a reminder that today is another special day; {sbj(fake_now=FAKE_NOW).lower()}\nand here's a look at notes from today in history."

def build_plain_text(notes, recipient_name, fake_now=None):
    text = build_dynamic_text(notes, fake_now)

    lines = [
        f"hi {recipient_name},",
        "",
        text,
        "",
    ]

    for note in notes:
        lines.append(f"{note['title']} – {note['url']}")

    return "\n".join(lines)

# ======= MAIN ======= #

def main():
    notes = load_notes()
    today_notes = filter_notes_for_today(notes, FAKE_NOW)

    cards_html = build_cards(today_notes)
    text = build_dynamic_text(today_notes, FAKE_NOW)
    subject = sbj(fake_now=FAKE_NOW)

    import tg_notif

    _, vibe = sbj(fake_now=FAKE_NOW)
    
    for email, name in recipients.items():

        plain_text = build_plain_text(today_notes, name, FAKE_NOW)

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
{cards_html}
<td align="center" style="width: 100%;padding: .75em 0 1em;"></td>
</tr>
</table>
</body>
</html>
"""

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
            


    # ======= TELEGRAM ======= #
    tg_notif.notify(
        subject=subject, 
        notes=today_notes, 
        vibe=vibe, 
        mode="milestone"
    )





if __name__ == "__main__":
    main()