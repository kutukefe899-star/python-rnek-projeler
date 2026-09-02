import requests

TOKEN = "8042571610:AAFu3CbtbfHm4h0S1LWIs46guy0ILdv8n-k"  # tırnak var
CHAT_ID = "8560293782"   # tırnak var

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