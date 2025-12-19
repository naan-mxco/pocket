import os
import random
import requests
from datetime import datetime



# --- CONFIGURATION ---

DRY_RUN = True  # True for Dry run, False to send
FAKE_NOW = datetime.now()
# FAKE_NOW = datetime(2025, 12, 19)
TELEGRAM_TARGETS = [
    "7465305123" #tonii
    # "1824489857" #bola
    # "6723013812" #t.a.
    # "-1003399218448" #pocket channel
    ]



def notify(subject, notes=None, vibe="low", mode="milestone", custom_text=None):
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    has_notes = notes is not None and (isinstance(notes, dict) or len(notes) > 0)
    
    catalog = {
        "milestone": {
            "high": [
                "<b>{s}</b>\n\n🥂 this is a big one! here are some memories:",
                "<b>{s}</b>\n\n✨ a truly special day. let's take a look back in time:",
                "<b>{s}</b>\n\n🎉 celebrating today!"
            ],
            "mid": [
                "<b>{s}</b>\n\n🎈 another big one! check today's notes from before:",
                "<b>{s}</b>\n\n🗓️ it's that time again! here's the archive:",
                "<b>{s}</b>\n\n✨ thinking of this today..."
            ],
            "low": [
                "<b>{s}</b>\n\n👋 just a quick check-in from your archive:",
                "<b>{s}</b>\n\n📖 here is your daily note:",
                "<b>{s}</b>\n\n✉️ found this in the pocket for you!"
            ]
        },

        "new_note": {
        "high": [
            "<b>{s}</b>\n\n✨ a special memory was just launched into your pocket! 🥂",
            "<b>{s}</b>\n\n🎉 something you might want to see was just archived. check it out!",
            "<b>{s}</b>\n\n💌 a new love letter has arrived in the pocket..."
        ],
        "mid": [
                "<b>{s}</b>\n\n🌟 something new moment to see is in the pocket!",
                "<b>{s}</b>\n\n🌻 adding to the archives... check what's new!",
                "<b>{s}</b>\n\n🎈 something special was just tucked away for you."
            ],
        "low": [
            "<b>{s}</b>\n\n🚀 a new note was just launched into your pocket!",
            "<b>{s}</b>\n\n📝 new note in the pocket!",
            "<b>{s}</b>\n\n👋 a special note for you",
            "<b>{s}</b>\n\n📥 something new...",
            "<b>{s}</b>\n\n💬 incoming message from the pocket"
        ]
    }
    }



    # 1. GREETING TEXT
    if custom_text:
        greeting = f"<b>{subject}</b>\n\n{custom_text}"
    elif mode == "milestone" and (notes is None or len(notes) == 0):
        if vibe in ["high", "mid"]:
            no_note_choices = [
                "<b>{s}</b>\n\n✨ special day, even with no notes in history today!",
                "<b>{s}</b>\n\n🌟 marking the occasion! no past notes found for today, but hiii"
                "<b>{s}</b>\n\n🌻 lovely day to celebrate! no history here yet, but we're remembering today.",
                "<b>{s}</b>\n\n🎈 it's a special one! the archive is empty for today, but the vibe is just right."
            ]
        else:
            no_note_choices = [
                "<b>{s}</b>\n\n🍃 quiet day in the archives. no old notes to show, just the beauty of today!",
                "<b>{s}</b>\n\n💎 this date is precious! even without past notes, we're celebrating."
            ]
        greeting = random.choice(no_note_choices).format(s=subject)
    else:
        category = catalog.get(mode, catalog["milestone"])
        choices = category.get(vibe, category.get("low"))
        greeting = random.choice(choices).format(s=subject)



    # 2. BUTTONS
    buttons = []
    if has_notes:
        note_list = [notes] if isinstance(notes, dict) else notes
        for n in note_list:
            buttons.append([{"text": f"📜 {n['title']}", "url": n.get('url', '#')}])
    
    # home button
    buttons.append([{"text": "check pocket", "url": "https://naan-mxco.github.io/pocket/"}])



    # 3. DELIVERY
    if DRY_RUN:
        print(f"\n[DRY RUN] Mode: {mode.upper()} | Vibe: {vibe.upper()}")
        print(f"Message: {greeting.replace('<b>','').replace('</b>','')}")
        for row in buttons:
            for btn in row:
                print(f"  BUTTON: {btn['text']} -> {btn['url']}")
    else:
        if not token:
            print("Error: Missing TELEGRAM_BOT_TOKEN")
            return
            
        for chat_id in TELEGRAM_TARGETS:
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            payload = {
                "chat_id": chat_id, 
                "text": greeting, 
                "parse_mode": "HTML", 
                "reply_markup": {"inline_keyboard": buttons}
            }
            try:
                r = requests.post(url, json=payload, timeout=30)
                status = "✅ Sent" if r.status_code == 200 else f"❌ Failed ({r.status_code})"
                print(f"Telegram ({chat_id}): {status}")
                if r.status_code != 200: print(f"   Response: {r.text}")
            except Exception as e:
                print(f"⚠️ Telegram Connection Error: {e}")





if __name__ == "__main__":
    # ======= TEST WITH cron_mailer ======= #
    try:
        from mail_utils import sbj
        from cron_mailer import load_notes, filter_notes_for_today
        
        print(f"--- Running Test for Date: {FAKE_NOW.strftime('%Y-%m-%d')} ---")
        
        notes_metadata = load_notes()
        todays_notes = filter_notes_for_today(notes_metadata, FAKE_NOW)
        subject, vibe = sbj(fake_now=FAKE_NOW)
        
        notify(
            subject=subject, 
            notes=todays_notes, 
            vibe=vibe, 
            mode="milestone"
        )
        
    except ImportError:
        print("Note: Run this in the same folder as cron_mailer.py to test with real JSON data.")
        notify("TEST SUBJECT", vibe="high", mode="milestone")