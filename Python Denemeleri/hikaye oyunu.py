import tkinter as tk
from tkinter import messagebox
from time import sleep

class TextAdventureGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Metin Tabanlı Hikaye Oyunu")
        self.geometry("400x400")

        self.current_text = tk.StringVar()
        self.current_text.set("Metin Tabanlı Hikaye Oyunu\n\nBu Oyun Kullanıcının Seçimine Göre İlerler.\nÖn Hikaye:\n")

        self.label = tk.Label(self, textvariable=self.current_text, wraplength=380, justify=tk.LEFT, padx=10, pady=10)
        self.label.pack()

        self.entry_frame = tk.Frame(self)
        self.entry_frame.pack(pady=10)

        self.entry_label = tk.Label(self.entry_frame, text="Karakter Adınızı Giriniz:")
        self.entry_label.pack(side=tk.LEFT, padx=10)

        self.karakter_entry = tk.Entry(self.entry_frame, width=20)
        self.karakter_entry.pack(side=tk.LEFT, padx=10)
        self.karakter_entry.bind("<Return>", lambda event: self.start_game())

        self.start_button = tk.Button(self.entry_frame, text="Oyuna Başla", command=self.start_game)
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.choice_frame = tk.Frame(self)
        self.choice_frame.pack(pady=20)

        self.buttons = []

    def start_game(self):
        karakter = self.karakter_entry.get()
        if not karakter:
            messagebox.showwarning("Uyarı", "Lütfen bir karakter adı girin!")
            return

        self.current_text.set(f"Merhaba, {karakter}. Sen hayatını normal olarak yaşayan sıradan bir insansın, ama bir gün hayatın eskisi kadar normal olamayacak bir güne uyandın.")
        self.update()
        self.after(3000, self.bolum1)  # 3 saniye bekledikten sonra bölüm 1'e geç

        self.entry_frame.pack_forget()  # Entry frame'i gizle

    def bolum1(self):
        self.current_text.set("\nBölüm 1: Herkes Nerede?\nYatağından kalktın ve evden hiçbir ses gelmiyor.")
        self.update()
        self.secim_yap_bolum1()

    def secim_yap_bolum1(self):
        self.clear_buttons()
        secenekler = [
            "Eşini ara",
            "Çocukların odasına git",
            "Dışarı bak"
        ]

        for secim in secenekler:
            button = tk.Button(self.choice_frame, text=secim, width=30, command=lambda s=secim: self.handle_choice_bolum1(s))
            button.pack(pady=5)
            button.bind("<Return>", lambda event, s=secim: self.handle_choice_bolum1(s))
            self.buttons.append(button)

    def handle_choice_bolum1(self, secim):
        self.clear_buttons()
        if secim == "Eşini ara":
            self.current_text.set("Eşini aramaya karar verdin. Telefonunu çıkarıp aramaya başladın.")
            self.update()
            sleep(1)
            self.current_text.set("...........................................")
            self.update()
            sleep(4)
            self.current_text.set("Telefona ulaşılamıyor.")
            self.update()
            self.after(2000, self.secim_yap_bolum3)
        elif secim == "Çocukların odasına git":
            self.current_text.set("Çocukların odasına gitmeye karar verdin.")
            self.update()
            sleep(0.5)
            self.current_text.set(".............................")
            self.update()
            sleep(1)
            self.current_text.set("Kapıyı açtın ve çocuklar odasında değil.")
            self.update()
            self.after(2000, self.secim_yap_bolum2)
        elif secim == "Dışarı bak":
            self.current_text.set("Dışarıya bakmaya karar verdin.")
            self.update()
            sleep(1)
            self.current_text.set("Dışarıya baktın ve kimse yok...")
            self.update()
            self.after(2000, self.secim_yap_bolum3)

    def secim_yap_bolum2(self):
        self.clear_buttons()
        secenekler = [
            "Eşini Ara",
            "Dışarıya çık"
        ]

        for secim in secenekler:
            button = tk.Button(self.choice_frame, text=secim, width=30, command=lambda s=secim: self.handle_choice_bolum2(s))
            button.pack(pady=5)
            button.bind("<Return>", lambda event, s=secim: self.handle_choice_bolum2(s))
            self.buttons.append(button)

    def handle_choice_bolum2(self, secim):
        self.clear_buttons()
        if secim == "Eşini Ara":
            self.current_text.set("Eşini aramaya karar verdin. Telefonunu çıkarıp aramaya başladın.")
            self.update()
            sleep(1)
            self.current_text.set("...........................................")
            self.update()
            sleep(4)
            self.current_text.set("Telefona ulaşılamıyor.")
            self.update()
            self.after(2000, self.secim_yap_bolum2)
        elif secim == "Dışarıya çık":
            self.current_text.set("Dışarıya çıkmaya karar verdin.")
            self.update()
            sleep(1)
            self.current_text.set("Kapıyı açtın ve dışarıya çıktın.")
            self.update()

    def secim_yap_bolum3(self):
        self.clear_buttons()
        secenekler = [
            "Çocuklarının odasına git",
            "Dışarıya çık"
        ]

        for secim in secenekler:
            button = tk.Button(self.choice_frame, text=secim, width=30, command=lambda s=secim: self.handle_choice_bolum3(s))
            button.pack(pady=5)
            button.bind("<Return>", lambda event, s=secim: self.handle_choice_bolum3(s))
            self.buttons.append(button)

    def handle_choice_bolum3(self, secim):
        self.clear_buttons()
        if secim == "Çocuklarının odasına git":
            self.current_text.set("Çocukların odasına gitmeye karar verdin.")
            self.update()
            sleep(0.5)
            self.current_text.set(".............................")
            self.update()
            sleep(1)
            self.current_text.set("Kapıyı açtın ve çocuklar odasında değil.")
            self.update()
            self.after(2000, self.secim_yap_bolum3)
        elif secim == "Dışarıya çık":
            self.current_text.set("Dışarıya çıkmaya karar verdin.")
            self.update()
            sleep(1)
            self.current_text.set("Kapıyı açtın ve dışarıya çıktın.")
            self.update()

    def clear_buttons(self):
        for button in self.buttons:
            button.pack_forget()
        self.buttons = []

if __name__ == "__main__":
    app = TextAdventureGame()
    app.mainloop()
