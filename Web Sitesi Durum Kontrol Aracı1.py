import requests
import webbrowser
import json
from datetime import datetime
import tkinter as tk  
from tkinter import messagebox 

def siteyi_kontrol_et():
    adres = adres_girisi.get()
    
    if adres == "":
        messagebox.showwarning("Uyarı", "Lütfen kontrol edilecek bir adres girin!")
        return

    if not adres.startswith("http://") and not adres.startswith("https://"):
        adres = "https://" + adres

    durum_etiketi.config(text="Bağlanılıyor... Lütfen bekleyin.", fg="blue")
    pencere.update() 

    try:
        cevap = requests.get(adres, timeout=5)
        durum_kodu = cevap.status_code
        
        if durum_kodu == 200:
            durum_mesaji = "Site sorunsuz çalışıyor! (200 OK)"
            renk = "green"
        elif durum_kodu == 403:
            durum_mesaji = "Erişim reddedildi. (403 Forbidden)"
            renk = "orange"
        elif durum_kodu == 404:
            durum_mesaji = "Sayfa bulunamadı. (404 Not Found)"
            renk = "red"
        elif durum_kodu == 500:
            durum_mesaji = "Sunucu hatası var. (500 Internal Error)"
            renk = "red"
        else:
            durum_mesaji = f"Farklı bir durum kodu: {durum_kodu}"
            renk = "black"

        durum_etiketi.config(text=durum_mesaji, fg=renk)

        rapor_verisi = {
            "kontrol_tarihi": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "istek_yapilan_adres": adres,
            "alinan_durum_kodu": durum_kodu,
            "sonuc_mesaji": durum_mesaji
        }
        with open("son_kontrol.json", "w", encoding="utf-8") as dosya:
            json.dump(rapor_verisi, dosya, ensure_ascii=False, indent=4)

        if durum_kodu == 200:
            webbrowser.open(adres)

    except requests.exceptions.Timeout:
        durum_etiketi.config(text="Bağlantı Hatası: Zaman aşımı!", fg="red")
    except requests.exceptions.RequestException:
        durum_etiketi.config(text="Bağlantı Hatası: Siteye ulaşılamadı.", fg="red")

pencere = tk.Tk()
pencere.title("Web Durum Kontrol Aracı") 
pencere.geometry("400x250") 

baslik = tk.Label(pencere, text="Web Sitesi Kontrol Aracı", font=("Arial", 14, "bold"))
baslik.pack(pady=15)

adres_girisi = tk.Entry(pencere, width=40, font=("Arial", 11))
adres_girisi.pack(pady=5)
adres_girisi.insert(0, "google.com") 

kontrol_butonu = tk.Button(pencere, text="Siteyi Kontrol Et", font=("Arial", 11, "bold"), bg="#4CAF50", fg="white", command=siteyi_kontrol_et)
kontrol_butonu.pack(pady=15)

durum_etiketi = tk.Label(pencere, text="Durum: Bekleniyor...", font=("Arial", 11))
durum_etiketi.pack(pady=10)

pencere.mainloop()