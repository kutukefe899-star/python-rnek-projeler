import os
import sys
import time
import shutil
import platform
import webbrowser
import tempfile
import json
import random
import hashlib
import socket
import subprocess
from datetime import datetime

# HTML yerel sunucu kütüphaneleri
from threading import Thread
from http.server import SimpleHTTPRequestHandler
import socketserver

STORAGE_FILE = "toolbox_storage.json"

def local_storage_yaz(anahtar, deger):
    veri = {}
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                veri = json.load(f)
        except Exception: veri = {}
    veri[anahtar] = deger
    with open(STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(veri, f, ensure_ascii=False, indent=4)

def local_storage_oku(anahtar):
    if os.path.exists(STORAGE_FILE):
        try:
            with open(STORAGE_FILE, "r", encoding="utf-8") as f:
                veri = json.load(f)
                return veri.get(anahtar, None)
        except Exception: return None
    return None

def temizle():
    os.system('clear' if os.name == 'posix' else 'cls')

def siber_banner():
    print("\033[38;5;82m" + "┌" + "─"*57 + "┐")
    print("│⚡ REALME 10 SYSTEM SENSOR & TOOLBOX v5.5 [ZERO-CRASH] ⚡│")
    print("└" + "─"*57 + "┘" + "\033[0m")

# =====================================================================
# SENSÖR VE DONANIM PANEL TETİKLEYİCİLERİ (ANDROID ONAYLI)
# =====================================================================
def android_panel_tetikle(panel_turu):
    """webbrowser.open çökmelerini önlemek için am start komutlarını kullanır"""
    intent_haritasi = {
        "wifi": "android.settings.WIFI_SETTINGS",
        "bluetooth": "android.settings.BLUETOOTH_SETTINGS",
        "batarya": "android.intent.action.POWER_USAGE_SUMMARY"
    }
    action = intent_haritasi.get(panel_turu)
    if action:
        try:
            # Android Activity Manager üzerinden ayarlar panelini doğrudan çağırır
            subprocess.Popen(["am", "start", "-a", action], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("\033[92m[✓] Sistem paneli başarıyla tetiklendi.\033[0m")
        except Exception:
            print("\033[91m[-] Komut satırı erişimi kısıtlandı. Lütfen Ayarlar'dan manuel açın.\033[0m")

def direkt_ram_oku():
    try:
        with open('/proc/meminfo', 'r') as f:
            satirlar = f.readlines()
        toplam_kb = 0; bos_kb = 0
        for satir in satirlar:
            if 'MemTotal' in satir: toplam_kb = int(satir.split()[1])
            elif 'MemAvailable' in satir: bos_kb = int(satir.split()[1])
        toplam_gb = toplam_kb / (1024 * 1024)
        bos_gb = bos_kb / (1024 * 1024)
        return toplam_gb, toplam_gb - bos_gb, bos_gb
    except Exception:
        return None, None, None

def direkt_pil_ve_termal_oku():
    sistem_bilgisi = {
        "yuzde": "Bilinmiyor", "durum": "Bilinmiyor", "batarya_temp": "Bilinmiyor", "cihaz_temp": "Bilinmiyor"
    }
    try:
        cikti = subprocess.check_output(["dumpsys", "battery"], stderr=subprocess.DEVNULL).decode("utf-8")
        for satir in cikti.split("\n"):
            if "level:" in satir: sistem_bilgisi["yuzde"] = satir.split(":")[1].strip() + "%"
            elif "status:" in satir:
                sistem_bilgisi["durum"] = "Şarj Oluyor ⚡" if satir.split(":")[1].strip() == "2" else "Deşarj Oluyor 🔋"
            elif "temperature:" in satir:
                sistem_bilgisi["batarya_temp"] = f"{int(satir.split(':')[-1].strip()) / 10}°C"
    except Exception: pass

    try:
        for i in range(0, 60):
            type_yol = f'/sys/class/thermal/thermal_zone{i}/type'
            temp_yol = f'/sys/class/thermal/thermal_zone{i}/temp'
            if os.path.exists(type_yol) and os.path.exists(temp_yol):
                with open(type_yol, 'r') as f: sensor_tipi = f.read().strip().lower()
                if any(x in sensor_tipi for x in ['cpu', 'mtktscpu', 'battery', 'bms', 'soc', 'pmic']):
                    with open(temp_yol, 'r') as f:
                        t_val = int(f.read().strip())
                        if t_val > 1000: t_val = t_val / 1000
                        if 0 < t_val < 100:
                            sistem_bilgisi["cihaz_temp"] = f"{t_val:.1f}°C"
                            if "cpu" in sensor_tipi: break
    except Exception: pass
    return sistem_bilgisi

# =====================================================================
# SİBER MODÜLLER
# =====================================================================

def mod_1_telemetri():
    temizle(); siber_banner()
    print("\033[94m[1] CANLI ÇEKİRDEK RAM & TELEMETRİ\033[0m\n")
    print(f"[+] İşletim Sistemi : Android (Kernel: {platform.release()})")
    t_ram, k_ram, b_ram = direkt_ram_oku()
    if t_ram: print(f"[+] Canlı RAM       : Toplam: {t_ram:.2f} GB | Kullanılan: {k_ram:.2f} GB")
    input("\nDevam etmek için ENTER...")

def mod_2_ai_asistan():
    temizle(); siber_banner(); print("\033[94m[2] AI SİBER ASİSTAN [GROQ L-STORE]\033[0m\n")
    key = local_storage_oku("groq_api_key")
    if key:
        print("\033[92m[✓] Kayıtlı API Anahtarı Algılandı.\033[0m")
        sec = input("Değiştirmek için 'd' yazın, geçmek için ENTER: ").strip()
        if sec.lower() == 'd': key = input("Yeni Anahtar: ").strip(); local_storage_yaz("groq_api_key", key)
    else:
        key = input("Groq API Anahtarını Girin: ").strip()
        if key: local_storage_yaz("groq_api_key", key)
        else: return
    print("\nAI Aktif. Çıkmak için 'cik' yazın.")
    try:
        import requests
    except ImportError: print("[-] requests modülü eksik!"); input(); return
    while True:
        soru = input("\nSoru > ")
        if soru.lower() == 'cik': break
        if not soru.strip(): continue
        print("Düşünüyor... 🧠")
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
            body = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": soru}]}
            res = requests.post(url, headers=headers, json=body)
            if res.status_code == 200: print("\n\033[96m[Cevap]:\033[0m\n" + res.json()['choices'][0]['message']['content'])
            else: print(f"Hata: {res.status_code}")
        except Exception as e: print(f"Bağlantı Hatası: {e}")

def mod_3_html_server():
    """SyntaxError ve file:// hatası giderilmiş sunucu önizleme sistemi"""
    temizle(); siber_banner(); print("\033[94m[3] HTML KOD CANLI ÖNİZLEME (WEB)\033[0m\n")
    print("[!] HTML kodunu yapıştırın (Bitirmek için boş satırda ENTER):\n")
    satirlar = []
    while True:
        s = input()
        if s == "": break
        satirlar.append(s)
    html_icerik = "\n".join(satirlar)
    if not html_icerik.strip(): return
    gecici_dizin = tempfile.mkdtemp()
    with open(os.path.join(gecici_dizin, "index.html"), "w", encoding="utf-8") as f: f.write(html_icerik)
    port = random.randint(8000, 8999)
    os.chdir(gecici_dizin)
    
    def sunucu():
        # Görsel 8'deki sözdizimi (Syntax) hatası düzeltildi
        try:
            handler = SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", port), handler) as httpd:
                httpd.serve_forever()
        except Exception:
            pass

    Thread(target=sunucu, daemon=True).start()
    time.sleep(0.6)
    # file:// yerine yerel ağ protokolü zorlanır (Görsel 1 Çözümü)
    webbrowser.open(f"http://127.0.0.1:{port}")
    print(f"\033[92m[✓] Local sunucu başlatıldı: http://127.0.0.1:{port}\033[0m")
    input("\nKapatmak için ENTER...")

def mod_4_link_ayikla():
    temizle(); siber_banner(); print("\033[94m[4] METİN İÇİNDEN LİNK AYIKLAYICI\033[0m\n")
    print("Metni yapıştırın (Boş satırda ENTER):")
    kod = []
    while True:
        s = input()
        if s == "": break
        kod.append(s)
    import re
    linkler = re.findall(r'(https?://[^\s"\']+)', "\n".join(kod))
    if linkler:
        for l in linkler: print(f"[+] Algılandı ve Açılıyor: {l}"); webbrowser.open(l)
    else: print("Link bulunamadı.")
    input("\nDevam etmek için ENTER...")

def mod_5_ag_bilgisi():
    temizle(); siber_banner(); print("\033[94m[5] TELEFON LOKAL IP & AĞ BİLGİSİ\033[0m\n")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        print(f"[+] Telefon Lokal IP Adresi: {s.getsockname()[0]}")
        s.close()
    except Exception: print("Ağ bağlantısı okunamadı.")
    input("\nDevam etmek için ENTER...")

def mod_6_wifi_tetikle():
    temizle(); siber_banner(); print("\033[94m[6] WI-FI DONANIM PANELİNİ TETİKLE\033[0m\n")
    android_panel_tetikle("wifi")
    input("\nDevam etmek için ENTER...")

def mod_7_bluetooth_tetikle():
    temizle(); siber_banner(); print("\033[94m[7] BLUETOOTH DONANIM PANELİNİ TETİKLE\033[0m\n")
    android_panel_tetikle("bluetooth")
    input("\nDevam etmek için ENTER...")

def mod_8_guc_isi_analiz():
    temizle(); siber_banner(); print("\033[94m[8] CANLI GÜÇ, BATARYA & ISI ANALİZİ\033[0m\n")
    veri = direkt_pil_ve_termal_oku()
    print(f"[+] Pil Seviyesi       : {veri['yuzde']}")
    print(f"[+] Şarj Durumu        : {veri['durum']}")
    print(f"[+] Batarya Sıcaklığı  : {veri['batarya_temp']}")
    print(f"[+] Anakart / CPU Isısı: {veri['cihaz_temp']}")
    input("\nDevam etmek için ENTER...")

def mod_9_sifre_uretici():
    temizle(); siber_banner(); print("\033[94m[9] GÜVENLİ SİBER ŞİFRE ÜRETİCİ\033[0m\n")
    havuz = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+="
    print(f"\033[92m[Üretilen Şifre]:\033[0m {''.join(random.choice(havuz) for _ in range(16))}")
    input("\nDevam etmek için ENTER...")

def mod_10_tahmin_oyunu():
    """Görsel 3'teki NameError hatası tamamen düzeltilmiş oyun yapısı"""
    temizle(); siber_banner(); print("\033[94m[10] SAYI TAHMİN OYUNU (STRES ATMA MODU)\033[0m\n")
    h = random.randint(1, 100)
    print("1 ile 100 arasında bir sayı tuttum. Tahmin et!")
    while True:
        t = input("Tahmininiz: ").strip()
        if not t.isdigit(): continue
        t = int(t)
        if t < h: print("Daha büyük!")
        elif t > h: print("Daha küçük!")
        else: print("\033[92m[✓] Tam isabet!\033[0m"); break
    input("\nDevam etmek için ENTER...")

def mod_11_kripto_hash():
    temizle(); siber_banner(); print("\033[94m[11] METİN KRİPTO HASH (MD5/SHA256)\033[0m\n")
    metin = input("Metni girin: ")
    if metin:
        print(f"[+] MD5    : {hashlib.md5(metin.encode()).hexdigest()}")
        print(f"[+] SHA256 : {hashlib.sha256(metin.encode()).hexdigest()}")
    input("\nDevam etmek için ENTER...")

def mod_12_dunya_saatleri():
    temizle(); siber_banner(); print("\033[94m[12] DÜNYA SAATLERİ SENKRONİZASYONU\033[0m\n")
    now = datetime.now()
    print(f"[+] Yerel Zaman (TR)  : {now.strftime('%H:%M:%S')} | Epoch: {int(time.time())}")
    input("\nDevam etmek için ENTER...")

def mod_13_kronometre():
    temizle(); siber_banner(); print("\033[94m[13] HASSAS SİBER SAYAÇ / KRONOMETRE\033[0m\n")
    print("[+] Başlatmak için ENTER'a basın. Durdurmak için CTRL+C yapın.")
    input()
    b = time.time()
    try:
        while True:
            print(f"\r⏱️ Süre: {time.time() - b:.2f} sn", end="", flush=True)
            time.sleep(0.1)
    except KeyboardInterrupt: print(f"\n\n[✓] Durduruldu. Total: {time.time() - b:.2f} sn")
    input("\nDevam etmek için ENTER...")

def mod_14_2048_oyunu():
    temizle(); siber_banner(); print("\033[94m[14] DOKUNMATİK 2048 SİBER OYUN MOTORU\033[0m\n")
    html_2048 = """<!DOCTYPE html><html><head><meta charset="UTF-8"><title>2048</title><style>body{background:#121212;color:#fff;text-align:center;font-family:sans-serif;}#board{width:280px;height:280px;background:#282a36;margin:10px auto;display:grid;grid-template-columns:repeat(4,1fr);gap:5px;padding:5px;border-radius:5px;}.cell{background:#44475a;display:flex;justify-content:center;align-items:center;font-size:20px;font-weight:bold;border-radius:4px;height:65px;}</style></head><body><h1>2048 Touch</h1><div id="board"></div><script>let b=Array(16).fill(0);function d(){let c=document.getElementById("board");c.innerHTML="";b.forEach(v=>{let e=document.createElement("div");e.className="cell";e.innerText=v?v:"";c.appendChild(e);});}b[0]=2;b[1]=2;window.onload=d;</script></body></html>"""
    g = tempfile.mkdtemp()
    with open(os.path.join(g, "index.html"), "w") as f: f.write(html_2048)
    port = random.randint(9000, 9999); os.chdir(g)
    Thread(target=lambda: socketserver.TCPServer(("", port), SimpleHTTPRequestHandler).serve_forever(), daemon=True).start()
    time.sleep(0.5); webbrowser.open(f"http://127.0.0.1:{port}")
    input("\nGeri dönmek için ENTER...")

def mod_15_depolama_analiz():
    temizle(); siber_banner(); print("\033[94m[15] TELEFON SÜRÜCÜ & DEPOLAMA ANALİZİ\033[0m\n")
    yol = "/storage/emulated/0" if os.path.exists("/storage/emulated/0") else "/"
    try:
        t, k, b = shutil.disk_usage(yol)
        print(f"[+] Toplam Alan : {t/(1024**3):.2f} GB | Boş Alan: {b/(1024**3):.2f} GB")
    except Exception: print("Depolama okunamadı.")
    input("\nDevam etmek için ENTER...")

def mod_16_pil_paneli_tetikle():
    temizle(); siber_banner(); print("\033[94m[16] PİL VE GÜÇ YÖNETİM PANELİ\033[0m\n")
    android_panel_tetikle("batarya")
    input("\nDevam etmek için ENTER...")

def mod_17_binary_codec():
    temizle(); siber_banner(); print("\033[94m[17] BINARY KOD OLUŞTURUCU / ÇÖZÜCÜ\033[0m\n")
    print(" [1] Metni Binary Koda Çevir\n [2] Binary Kodu Metne Çevir")
    sec = input("\nSeçim > ").strip()
    if sec == "1":
        m = input("Metin: ")
        print("\n[Sonuç]:", ' '.join(format(ord(x), '08b') for x in m))
    elif sec == "2":
        b = input("Binary Kod: ").strip().replace(" ", "")
        try:
            bloklar = [b[i:i+8] for i in range(0, len(b), 8)]
            print("\n[Çözülen]:", "".join(chr(int(x, 2)) for x in bloklar if len(x) == 8))
        except Exception: print("[-] Hatalı binary dizilimi.")
    input("\nDevam etmek için ENTER...")

def mod_17_metin_sayici():
    temizle(); siber_banner(); print("\033[94m[17] METİN VE SATIR SAYICI MOTORU\033[0m\n")
    print("Metni yapıştırın (ENTER ile bitirin):")
    s = []
    while True:
        i = input()
        if i == "": break
        s.append(i)
    print(f"\n[+] Satır: {len(s)} | Karakter: {len(''.join(s))}")
    input("\nDevam etmek için ENTER...")

def mod_18_url_codec():
    temizle(); siber_banner(); print("\033[94m[18] URL ENCODER / DECODER ENJEKTÖRÜ\033[0m\n")
    from urllib.parse import quote, unquote
    m = input("URL girin: ")
    print(f"[+] Encoded: {quote(m)}\n[+] Decoded: {unquote(m)}")
    input("\nDevam etmek için ENTER...")

def mod_19_fake_data():
    temizle(); siber_banner(); print("\033[94m[19] DEVELOPER TEST VERİSİ ÜRETİCİ\033[0m\n")
    isler = ["Ahmet", "Can", "Efe", "Zeynep"]; soylar = ["Yılmaz", "Kaya", "Demir"]
    print(f"[+] Kimlik: {random.choice(isler)} {random.choice(soylar)}")
    input("\nDevam etmek için ENTER...")

def mod_20_matematik_cozucu():
    temizle(); siber_banner(); print("\033[94m[20] HIZLI MATEMATİKSEL EVAL MOTORU\033[0m\n")
    denklem = input("İfade girin: ")
    try:
        if all(c in "0123456789+-*/(). " for c in denklem): print(f"[✓] Sonuç: {eval(denklem)}")
        else: print("[-] Güvensiz karakter!")
    except Exception: print("[-] Hata.")
    input("\nDevam etmek için ENTER...")

def mod_21_base64_codec():
    temizle(); siber_banner(); print("\033[94m[21] BASE64 ENCODE / DECODER SİSTEMİ\033[0m\n")
    import base64
    sec = input("[1] Encode | [2] Decode: ")
    m = input("Girdi: ")
    try:
        if sec == "1": print("[+] Sonuç:", base64.b64encode(m.encode()).decode())
        else: print("[✓] Çözülen:", base64.b64decode(m.encode()).decode())
    except Exception: print("[-] Hata.")
    input("\nDevam etmek için ENTER...")

# =====================================================================
# ANA DÖNGÜ
# =====================================================================
while True:
    temizle(); siber_banner()
    print("🤖 CRASH-FREE SİBER PANEL MODÜL LİSTESİ:\n")
    print(" \033[38;5;226m[1]\033[0m RAM & Sistem Raporu          \033[38;5;226m[12]\033[0m Dünya Saatleri Senkronize")
    print(" \033[38;5;226m[2]\033[0m AI Asistan [Groq L-Store]     \033[38;5;226m[13]\033[0m Hassas Sayaç / Kronometre")
    print(" \033[38;5;226m[3]\033[0m HTML Kod Canlı Önizleme       \033[38;5;226m[14]\033[0m Dokunmatik 2048 Oyun Motoru")
    print(" \033[38;5;226m[4]\033[0m Metinden Link Ayıkla          \033[38;5;226m[15]\033[0m Depolama ve Sürücü Analizi")
    print(" \033[38;5;226m[5]\033[0m Telefon Lokal IP & Ağ Bilgisi \033[38;5;82m[16] Pil ve Güç Panelini Tetikle\033[0m")
    print(" \033[38;5;82m[6] Wi-Fi Panelini Zorla Tetikle\033[0m \033[38;5;82m[17] Binary Kod Çevirici/Çözücü\033[0m")
    print(" \033[38;5;82m[7] Bluetooth Panelini Tetikle\033[0m   \033[38;5;226m[18]\033[0m URL Encoder / Decoder")
    print(" \033[38;5;226m[8]\033[0m Canlı Güç, Batarya & Isı      \033[38;5;226m[19]\033[0m Developer Test Veri Üretici")
    print(" \033[38;5;226m[9]\033[0m Güvenli Şifre Üretici         \033[38;5;226m[20]\033[0m Matematiksel Eval Motoru")
    print(" \033[38;5;226m[10]\033[0m Sayı Tahmin Oyunu (Sabit)    \033[38;5;226m[21]\033[0m Base64 Şifreleme Sistemleri")
    print(" \033[38;5;226m[11]\033[0m Kripto Hash (MD5/SHA)         \033[38;5;196m[0] Sistemden Güvenli Çıkış\033[0m")
    
    secim = input("\n\033[38;5;45mSiber-Menu > \033[0m").strip()
    if secim == "1": mod_1_telemetri()
    elif secim == "2": mod_2_ai_asistan()
    elif secim == "3": mod_3_html_server()
    elif secim == "4": mod_4_link_ayikla()
    elif secim == "5": mod_5_ag_bilgisi()
    elif secim == "6": mod_6_wifi_tetikle()
    elif secim == "7": mod_7_bluetooth_tetikle()
    elif secim == "8": mod_8_guc_isi_analiz()
    elif secim == "9": mod_9_sifre_uretici()
    elif secim == "10": mod_10_tahmin_oyunu()
    elif secim == "11": mod_11_kripto_hash()
    elif secim == "12": mod_12_dunya_saatleri()
    elif secim == "13": mod_13_kronometre()
    elif secim == "14": mod_14_2048_oyunu()
    elif secim == "15": mod_15_depolama_analiz()
    elif secim == "16": mod_16_pil_paneli_tetikle()
    elif secim == "17": mod_17_binary_codec()
    elif secim == "18": mod_18_url_codec()
    elif secim == "19": mod_19_fake_data()
    elif secim == "20": mod_20_matematik_cozucu()
    elif secim == "21": mod_21_base64_codec()
    elif secim == "0": break

