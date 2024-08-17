import tkinter as tk
from tkinter import ttk, messagebox
import random
import os

# Rastgele skor tahmini fonksiyonu
def rastgele_skor_tahmini():
    return random.randint(0, 5), random.randint(0, 5)

# Oran tahmini ve skor kontrol fonksiyonu
def oran_tahmini_ve_skor_kontrol(maclar, oranlar, secilen_mac_id, secilen_oran, yatirilan_miktar):
    secilen_mac = None
    for mac, id in maclar.items():
        if id == secilen_mac_id:
            secilen_mac = mac
            break

    if secilen_mac is None:
        return "Geçersiz maç ID'si. Lütfen doğru bir ID girin."

    ev_sahibi_skor, misafir_skor = rastgele_skor_tahmini()

    oran_tuttu_mu = False
    if secilen_oran == "Ev Sahibi" and ev_sahibi_skor > misafir_skor:
        oran_tuttu_mu = True
    elif secilen_oran == "Misafir" and misafir_skor > ev_sahibi_skor:
        oran_tuttu_mu = True
    elif secilen_oran == "Beraberlik" and ev_sahibi_skor == misafir_skor:
        oran_tuttu_mu = True

    kazanilan_miktar = yatirilan_miktar * oranlar[secilen_mac][secilen_oran] if oran_tuttu_mu else 0

    return secilen_mac, ev_sahibi_skor, misafir_skor, oran_tuttu_mu, oranlar[secilen_mac][secilen_oran], kazanilan_miktar

# Rastgele oran oluşturma fonksiyonu
def oran_olustur(maclar):
    oranlar = {}
    for mac in maclar:
        ev_sahibi_oran = round(random.uniform(1.1, 3.0), 2)
        misafir_oran = round(random.uniform(1.1, 3.0), 2)
        beraberlik_oran = round(random.uniform(2.0, 4.0), 2)
        oranlar[mac] = {
            "Ev Sahibi": ev_sahibi_oran,
            "Misafir": misafir_oran,
            "Beraberlik": beraberlik_oran
        }
    return oranlar

# Bakiyeyi dosyadan okuma
def bakiye_yukle(dosya_adi):
    if os.path.exists(dosya_adi):
        with open(dosya_adi, "r") as dosya:
            return float(dosya.read().strip())
    return 1000.0  # Varsayılan başlangıç bakiyesi

# Bakiyeyi dosyaya yazma
def bakiye_kaydet(dosya_adi, bakiye):
    with open(dosya_adi, "w") as dosya:
        dosya.write(str(bakiye))

# Tkinter arayüzünü oluşturma
class IddeaProgrami:
    def __init__(self, root):
        self.root = root
        self.root.title("İddia Programı")
        self.bakiye_dosya_adi = "bakiye.txt"

        # Başlangıç bakiyesi
        self.bakiye = bakiye_yukle(self.bakiye_dosya_adi)

        # Bakiye göstergesi
        self.label_bakiye = tk.Label(root, text=f"Bakiye: {self.bakiye} TL", font=("Arial", 12, "bold"))
        self.label_bakiye.pack(pady=10)

        # Maç ve Oran seçimi için Frame oluşturalım
        self.frame_secim = tk.Frame(root)
        self.frame_secim.pack()

        self.label_baslik = tk.Label(self.frame_secim, text="İddia Programı")
        self.label_baslik.pack()

        self.label_secim = tk.Label(self.frame_secim, text="Maç ve Oran Seçin:")
        self.label_secim.pack()

        self.tree_maclar_oranlar = ttk.Treeview(self.frame_secim, columns=("Maç", "Ev Sahibi", "Misafir", "Beraberlik"), show="headings")
        self.tree_maclar_oranlar.heading("Maç", text="Maç")
        self.tree_maclar_oranlar.heading("Ev Sahibi", text="Ev Sahibi")
        self.tree_maclar_oranlar.heading("Misafir", text="Misafir")
        self.tree_maclar_oranlar.heading("Beraberlik", text="Beraberlik")

        self.tree_maclar_oranlar.pack()

        # Maçları tanımlayalım
        self.maclar = {
            "Real Madrid - Barcelona": 1,
            "Bayern Münich - Bayern Laverkusen": 2,
            "Fenerbahçe - Kasimpasa": 3,
            "Dortmund - Redbull Leipzig": 4,
            "Ankaragücü - Konyaspor": 5,
            "Real Socidead - Atletico Madrid": 6,
            "Hoffenheim - Wolfsburg": 7,
            "Köln - Mainz 05": 8,
            "Manchester City - Manchester United": 9
        }

        # Oranları oluşturalım
        self.oranlar = oran_olustur(self.maclar)

        for mac, id in self.maclar.items():
            ev_sahibi_oran = self.oranlar[mac]["Ev Sahibi"]
            misafir_oran = self.oranlar[mac]["Misafir"]
            beraberlik_oran = self.oranlar[mac]["Beraberlik"]
            self.tree_maclar_oranlar.insert("", "end", values=(mac, ev_sahibi_oran, misafir_oran, beraberlik_oran))

        self.label_yatirilan_miktar = tk.Label(self.frame_secim, text="Yatırılacak Miktar (TL):")
        self.label_yatirilan_miktar.pack()

        self.entry_yatirilan_miktar = tk.Entry(self.frame_secim)
        self.entry_yatirilan_miktar.pack()

        # Oran seçimi için tk.StringVar tanımlayalım
        self.var_oran_secim = tk.StringVar()

        self.label_oran_secim = tk.Label(self.frame_secim, text="Oran Seçin:")
        self.label_oran_secim.pack()

        self.rbutton_ev_sahibi = tk.Radiobutton(self.frame_secim, text="Ev Sahibi", variable=self.var_oran_secim, value="Ev Sahibi")
        self.rbutton_ev_sahibi.pack()

        self.rbutton_misafir = tk.Radiobutton(self.frame_secim, text="Misafir", variable=self.var_oran_secim, value="Misafir")
        self.rbutton_misafir.pack()

        self.rbutton_beraberlik = tk.Radiobutton(self.frame_secim, text="Beraberlik", variable=self.var_oran_secim, value="Beraberlik")
        self.rbutton_beraberlik.pack()

        self.button_tahmin = tk.Button(self.frame_secim, text="Tahmin Et", command=self.on_tahmin_et)
        self.button_tahmin.pack()

    def on_tahmin_et(self):
        secilen_mac_index = self.tree_maclar_oranlar.focus()
        if secilen_mac_index:
            secilen_mac = self.tree_maclar_oranlar.item(secilen_mac_index)['values'][0]
            secilen_oran = self.var_oran_secim.get()
            yatirilan_miktar = self.entry_yatirilan_miktar.get()

            if yatirilan_miktar.isdigit() and float(yatirilan_miktar) > 0:
                yatirilan_miktar = float(yatirilan_miktar)
                if yatirilan_miktar > self.bakiye:
                    messagebox.showerror("Hata", "Yeterli bakiyeniz yok.")
                    return

                onay = messagebox.askquestion("Tahmin Onayı", f"Bu tahmini yapmak istediğinizden emin misiniz?\n\n"
                                                               f"Maç: {secilen_mac}\n"
                                                               f"Yatırılan Miktar: {yatirilan_miktar} TL\n"
                                                               f"Seçilen Oran: {secilen_oran}")
                if onay == "yes":
                    secilen_mac_id = self.maclar[secilen_mac]
                    sonuc = oran_tahmini_ve_skor_kontrol(self.maclar, self.oranlar, secilen_mac_id, secilen_oran, yatirilan_miktar)
                    if isinstance(sonuc, tuple):
                        secilen_mac, ev_sahibi_skor, misafir_skor, oran_tuttu_mu, secilen_oran_degeri, kazanilan_miktar = sonuc
                        if oran_tuttu_mu:
                            self.bakiye += kazanilan_miktar
                        else:
                            self.bakiye -= yatirilan_miktar
                        
                        # Bakiyeyi güncelle ve kaydet
                        self.label_bakiye.config(text=f"Bakiye: {self.bakiye} TL")
                        bakiye_kaydet(self.bakiye_dosya_adi, self.bakiye)

                        messagebox.showinfo("Tahmin Sonucu", f"{secilen_mac}\n"
                                                             f"Skor: {ev_sahibi_skor} - {misafir_skor}\n"
                                                             f"Seçilen oran ({secilen_oran}): {secilen_oran_degeri}\n"
                                                             f"Kazanılan miktar: {kazanilan_miktar} TL" if oran_tuttu_mu else
                                                             f"Tahmin tutmadı. Kaybedilen miktar: {yatirilan_miktar} TL")
                    else:
                        messagebox.showerror("Hata", sonuc)
                else:
                    messagebox.showinfo("Tahmin İptal Edildi", "Tahmin işlemi iptal edildi.")
            else:
                messagebox.showerror("Hata", "Lütfen geçerli bir miktar girin.")
        else:
            messagebox.showerror("Hata", "Lütfen bir maç seçin.")

# Uygulamayı başlatma
if __name__ == "__main__":
    root = tk.Tk()
    uygulama = IddeaProgrami(root)
    root.mainloop()