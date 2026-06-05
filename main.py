import tkinter as tk
from tkinter import ttk, messagebox
from db import baglan


def tabloyu_temizle():
    for item in tablo.get_children():
        tablo.delete(item)


def kolonlari_ayarla(kolonlar):
    tablo["columns"] = kolonlar
    for kolon in kolonlar:
        tablo.heading(kolon, text=kolon)
        tablo.column(kolon, width=150)


def ucuslari_listele():
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT ucus_kodu, kalkis_zamani, bos_koltuk_sayisi, taban_fiyat
        FROM ucuslar
    """)
    sonuc = cursor.fetchall()

    tabloyu_temizle()
    kolonlari_ayarla(("Uçuş Kodu", "Kalkış Zamanı", "Boş Koltuk", "Fiyat"))

    for satir in sonuc:
        tablo.insert("", tk.END, values=satir)

    conn.close()


def biletleri_listele():
    conn = baglan()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT bilet_id, ad_soyad, eposta, ucus_kodu, koltuk_no, toplam_tutar, durum
        FROM YolcuBiletRaporu
    """)
    sonuc = cursor.fetchall()

    tabloyu_temizle()
    kolonlari_ayarla(("Bilet ID", "Yolcu", "E-posta", "Uçuş Kodu", "Koltuk", "Tutar", "Durum"))

    for satir in sonuc:
        tablo.insert("", tk.END, values=satir)

    conn.close()


def yolcu_ekle():
    conn = baglan()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO kullanicilar (ad_soyad, eposta, telefon)
            VALUES (%s, %s, %s)
        """, (
            entry_ad.get(),
            entry_eposta.get(),
            entry_telefon.get()
        ))

        conn.commit()
        messagebox.showinfo("Başarılı", "Yolcu başarıyla eklendi.")

        entry_ad.delete(0, tk.END)
        entry_eposta.delete(0, tk.END)
        entry_telefon.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Hata", str(e))

    conn.close()
def bilet_iptal_et():

    conn = baglan()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            UPDATE biletler
            SET durum = 'Iptal Edildi'
            WHERE bilet_id = %s
        """, (entry_bilet_id.get(),))

        conn.commit()

        messagebox.showinfo(
            "Başarılı",
            "Bilet iptal edildi."
        )

        entry_bilet_id.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Hata", str(e))

    conn.close() 

pencere = tk.Tk()
pencere.configure(bg="#EAF4FF")
logo = tk.PhotoImage(file="assets/plane.png")
logo = logo.subsample(4, 4)

logo_label = tk.Label(
    pencere,
    image=logo
)

logo_label.pack(pady=5)
pencere.title("Uçak Bileti Takip Sistemi")
pencere.geometry("1400x800")
pencere.resizable(False, False)
pencere.configure(bg="#EAF4FF")

baslik = tk.Label(pencere, text="Uçak Bileti Takip Sistemi", font=("Arial", 20, "bold"),
fg="#1565C0",
bg="#EAF4FF")
baslik.pack(pady=10)

buton_frame = tk.Frame(pencere)
buton_frame.pack(pady=10)

tk.Button(buton_frame, text="Uçuşları Listele", command=ucuslari_listele, bg="#1976D2",
    fg="white",width=20 ).grid(row=0, column=0, padx=10)
tk.Button(buton_frame, text="Biletleri Listele", command=biletleri_listele,bg="#1976D2",
    fg="white", width=20 ).grid(row=0, column=1, padx=10)

form_frame = tk.Frame(pencere)
form_frame.pack(pady=10)
iptal_frame = tk.Frame(pencere)
iptal_frame.pack(pady=10)

tk.Label(
    iptal_frame,
    text="Bilet ID"
).grid(row=0,column=0)

entry_bilet_id = tk.Entry(iptal_frame, width=15, font=("Arial", 11), relief="solid", bd=1)


entry_bilet_id.grid(row=0,column=1,padx=5)

btn_iptal = tk.Button(
    iptal_frame,
    text="Bilet İptal Et",
    command=bilet_iptal_et,bg="#1976D2",
    fg="white",
    width=12
)

btn_iptal.grid(row=0,column=2,padx=10)

tk.Label(form_frame, text="Ad Soyad").grid(row=0, column=0)
entry_ad = tk.Entry(form_frame, width=25, font=("Arial", 11), relief="solid", bd=1)
entry_ad.grid(row=0, column=1, padx=5)

tk.Label(form_frame, text="E-posta").grid(row=0, column=2)
entry_eposta = tk.Entry(form_frame, width=25, font=("Arial", 11), relief="solid", bd=1)
entry_eposta.grid(row=0, column=3, padx=5)

tk.Label(form_frame, text="Telefon").grid(row=0, column=4)
entry_telefon = tk.Entry(form_frame, width=20, font=("Arial", 11), relief="solid", bd=1)
entry_telefon.grid(row=0, column=5, padx=5)

tk.Button(form_frame, text="Yolcu Ekle", command=yolcu_ekle, bg="#1976D2",
    fg="white",
    width=12).grid(row=0, column=6, padx=10)

tablo = ttk.Treeview(pencere, show="headings")
tablo.pack(fill="both", expand=True, padx=10, pady=10)

pencere.mainloop()
# Kaynak:
# Tkinter Treeview bileşeni için resmi Python dokümantasyonundan yararlanılmıştır.
# https://docs.python.org/3/library/tkinter.ttk.html
# Not:
# Arayüz geliştirme sürecinde OpenAI ChatGPT'den teknik destek alınmıştır.
