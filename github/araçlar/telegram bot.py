import requests

TOKEN = "senin api keyin"  # tırnak var
CHAT_ID = "senin telegram chat idin"   # tırnak var

def telegram_gonder(mesaj):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": mesaj
    }
    r = requests.post(url, data=data)
    print("Status Code:", r.status_code)  # Bunu ekle
    print("Cevap:", r.text)  # Bunu ekle
    
    sonuc = r.json()
    if sonuc["ok"]:
        print("Gönderildi")
    else:
        print("HATA:", sonuc["description"]) # Telegram hatayı söyler

telegram_gonder("kodd")
