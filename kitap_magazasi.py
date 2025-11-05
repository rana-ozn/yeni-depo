import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

# --- 1. VERİ SETİ (KİTAPLAR) ---
# Resim adının 1. Aşamada hazırladığınız dosyalarla EŞLEŞTİĞİNDEN emin olun!
KITAPLAR = [
    {"ad": "1984", "yazar": "George Orwell", "fiyat": 15.99, "resim": "kitap_1.png"},
    {"ad": "The Great Gatsby", "yazar": "F. Scott Fitzgerald", "fiyat": 12.50, "resim": "kitap_2.png"},
    {"ad": "To Kill a Mockingbird", "yazar": "Harper Lee", "fiyat": 14.75, "resim": "kitap_3.png"},
    {"ad": "Dune", "yazar": "Frank Herbert", "fiyat": 22.00, "resim": "kitap_4.png"},
    {"ad": "Sapiens: A Brief History...", "yazar": "Yuval Noah Harari", "fiyat": 25.40, "resim": "kitap_5.png"},
]

# --- 2. GLOBAL DEĞİŞKENLER ---
sepet = {}  # Sepet: {"Kitap Adı": Miktar}
resim_nesneleri = [] # Garbage Collection'dan korumak için liste

# --- 3. PENCERE KURULUMU ---
pencere = tk.Tk()
pencere.title("Uluslararası Kitap Mağazası")
pencere.geometry("1000x750") # Pencereyi biraz büyüttük
pencere.resizable(False, False) 

# Ürünleri gösterecek ana çerçeve
urun_ana_cerceve = tk.Frame(pencere, bg="#ecf0f1")
urun_ana_cerceve.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

# Sepet Bilgisi için üstteki çubuk (sabit kalacak)
sepet_bilgi_cercevesi = tk.Frame(pencere, bd=2, relief=tk.RIDGE, bg="#f9f9f9")
sepet_bilgi_cercevesi.pack(side=tk.BOTTOM, fill=tk.X, ipady=10)

# Sepet Sayacı Etiketi
sepet_sayaci_etiketi = tk.Label(sepet_bilgi_cerceves, text="Sepet: 0 Ürün ($0.00)", font=("Arial", 14, "bold"), fg="#2980b9", bg="#f9f9f9")
sepet_sayaci_etiketi.pack(side=tk.LEFT, padx=30)

# Satın Al Butonu
satin_al_butonu = tk.Button(sepet_bilgi_cerceves, text="Şimdi SATIN AL", font=("Arial", 12, "bold"), bg="#e74c3c", fg="white", state=tk.DISABLED, command=lambda: messagebox.showinfo("Ödeme", f"Toplam {sepet_sayaci_etiketi.cget('text').split('(')[1].strip(')')} tutarındaki siparişiniz onaylandı."))
satin_al_butonu.pack(side=tk.RIGHT, padx=30)

# --- 4. FONKSİYONLAR ---

def sepeti_guncelle():
    """Sepet içeriğini hesaplar ve arayüzdeki etiketi günceller."""
    toplam_urun = sum(sepet.values())
    toplam_tutar = 0.0

    for kitap_ad, miktar in sepet.items():
        # Fiyatı bulmak için ürün listesini kontrol et
        for kitap in KITAPLAR:
            if kitap["ad"] == kitap_ad:
                toplam_tutar += kitap["fiyat"] * miktar
                break
    
    sepet_sayaci_etiketi.config(text=f"Sepet: {toplam_urun} Ürün (${toplam_tutar:.2f})")
    
    # Satın al butonunun durumunu güncelle
    if toplam_urun > 0:
        satin_al_butonu.config(state=tk.NORMAL)
    else:
        satin_al_butonu.config(state=tk.DISABLED)


def sepete_ekle(kitap_adi):
    """Kitabı sepete ekler ve arayüzü günceller."""
    if kitap_adi in sepet:
        sepet[kitap_adi] += 1
    else:
        sepet[kitap_adi] = 1
    
    # messagebox.showinfo("Eklendi", f"'{kitap_adi}' sepete eklendi.") # Çok fazla popup açmasını engellemek için yorum satırında
    sepeti_guncelle()


def urun_kartlari_olustur():
    """Her kitap için görsel kartları oluşturur ve ekranda gösterir."""
    
    sutun = 0 # 5 kitap için 5 sütun kullanacağız

    for kitap in KITAPLAR:
        # Her kitap için ayrı bir çerçeve (kart) oluştur
        kart = tk.Frame(urun_ana_cerceve, bd=1, relief=tk.RIDGE, padx=10, pady=10, bg="white")
        kart.grid(row=0, column=sutun, padx=15, pady=15, sticky="n") # dikeyde üste yasla

        # 1. Resim Alanı
        try:
            img = Image.open(kitap["resim"])
            img = img.resize((150, 220), Image.Resampling.LANCZOS) # Kitap kapağı boyutuna uygun ayar
            kitap_gorsel = ImageTk.PhotoImage(img)
            resim_nesneleri.append(kitap_gorsel) # GC'den koru

            resim_etiketi = tk.Label(kart, image=kitap_gorsel)
            resim_etiketi.pack(pady=5)
            
        except FileNotFoundError:
            hata_etiketi = tk.Label(kart, text=f"[{kitap['ad']} Resim Yok]", fg="red", width=20, height=12)
            hata_etiketi.pack(pady=5)
        except Exception as e:
            hata_etiketi = tk.Label(kart, text=f"Resim Hatası:\n{e}", fg="red", width=20, height=12)
            hata_etiketi.pack(pady=5)
        
        # 2. Kitap Adı
        tk.Label(kart, text=kitap["ad"], font=("Arial", 12, "bold"), wraplength=140).pack(pady=2)

        # 3. Yazar
        tk.Label(kart, text=f"Yazar: {kitap['yazar']}", font=("Arial", 10, "italic")).pack(pady=2)

        # 4. Fiyat
        tk.Label(kart, text=f"${kitap['fiyat']:.2f}", font=("Arial", 14, "bold"), fg="#27ae60").pack(pady=5)

        # 5. Sepete Ekle Butonu
        ekle_buton = tk.Button(kart, 
                               text="➕ Sepete Ekle", 
                               command=lambda k=kitap["ad"]: sepete_ekle(k), 
                               bg="#3498db", 
                               fg="white", 
                               font=("Arial", 10, "bold"),
                               width=18)
        ekle_buton.pack(pady=10)

        sutun += 1


# --- 5. UYGULAMAYI BAŞLATMA ---

urun_kartlari_olustur()
sepeti_guncelle() 

pencere.mainloop()