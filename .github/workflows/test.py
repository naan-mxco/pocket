from pmail import send_mail
from naan_events import get_subject as sbj

recipients: dict = {
    # 'naan.mxco@gmail.com' : 'Naan-MxCo BeeTee',
    # 'bayodenancy111@gmail.com' : 'Bolanle Nancy',
    # 'toniiabudu@gmail.com' : 'Tonii Abudu',
    'auralex99@gmail.com' : 'Tee',
}

for recipient_mail, recipient_name in recipients.items():
        text: str = f"hi, {recipient_name},\nthis is a test!"
        anchor_link: str = "https://naan-mxco.github.io/pocket/pockets/2024-08/away_camp/test.html"
        send_mail(recipient_mail, recipient_name, sbj(recipient_mail), text, anchor_link)