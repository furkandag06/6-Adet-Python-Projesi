import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
import os
from datetime import datetime
import fitz  # PyMuPDF kütüphanesi

class BookManager:
    def read_book(self, file_path):
        if file_path.lower().endswith(".pdf"):
            return self.read_pdf(file_path)
        elif file_path.lower().endswith(".epub"):
            return "EPUB dosyası okunacak."  # EPUB dosyası okuma kodunu ekle
        else:
            return "Desteklenmeyen dosya formatı."

    def read_pdf(self, file_path):
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            return f"PDF dosyası okunurken bir hata oluştu: {str(e)}"

class NoteManager:
    def __init__(self):
        self.notes_file = "notes.json"
        if not os.path.exists(self.notes_file):
            with open(self.notes_file, 'w') as f:
                json.dump([], f)

    def save_note(self, note):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.notes_file, 'r') as f:
            notes = json.load(f)
        notes.append({"timestamp": timestamp, "content": note})
        with open(self.notes_file, 'w') as f:
            json.dump(notes, f, indent=4)

    def load_notes(self):
        with open(self.notes_file, 'r') as f:
            return json.load(f)

    def delete_note_by_index(self, index):
        with open(self.notes_file, 'r') as f:
            notes = json.load(f)
        if 0 <= index < len(notes):
            notes.pop(index)
        with open(self.notes_file, 'w') as f:
            json.dump(notes, f, indent=4)

    def update_note_title(self, index, new_title):
        with open(self.notes_file, 'r') as f:
            notes = json.load(f)
        if 0 <= index < len(notes):
            notes[index]['timestamp'] = new_title
        with open(self.notes_file, 'w') as f:
            json.dump(notes, f, indent=4)

class EBookReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("E-Kitap Okuyucu ve Yöneticisi")
        self.book_manager = BookManager()
        self.note_manager = NoteManager()

        # Ana GUI bileşenleri
        self.create_widgets()

    def create_widgets(self):
        # E-Kitap Aç butonu
        self.open_button = tk.Button(self.root, text="E-Kitap Aç", command=self.open_book)
        self.open_button.grid(row=0, column=0, columnspan=2, pady=10)

        # PDF içeriğinin görüneceği alan (Orta Bölme)
        self.text_area = tk.Text(self.root, wrap=tk.WORD, bg="white", fg="black")
        self.text_area.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.text_area.config(state=tk.DISABLED)

        # Notların yönetileceği alan (Sağ Bölme)
        self.note_frame = tk.Frame(self.root)
        self.note_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        self.note_text_area = tk.Text(self.note_frame, wrap=tk.WORD, bg="lightgray", fg="black")
        self.note_text_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.save_note_button = tk.Button(self.note_frame, text="Not Kaydet", command=self.save_note)
        self.save_note_button.grid(row=1, column=0, pady=5, sticky="ew")

        self.notes_listbox = tk.Listbox(self.note_frame)
        self.notes_listbox.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.notes_listbox.bind("<Double-1>", self.show_selected_note)
        self.notes_listbox.bind("<Button-3>", self.show_context_menu)

        self.delete_note_button = tk.Button(self.note_frame, text="Seçili Notu Sil", command=self.delete_selected_note)
        self.delete_note_button.grid(row=1, column=1, pady=5, padx=10, sticky="ew", columnspan=2)

        # Notlar frame grid ağı yapılandırması
        self.note_frame.columnconfigure(0, weight=1)
        self.note_frame.columnconfigure(1, weight=1)
        self.note_frame.rowconfigure(0, weight=1)
        self.note_frame.rowconfigure(1, weight=0)

        # Grid ağı yapılandırması
        self.root.columnconfigure(0, weight=2)
        self.root.columnconfigure(1, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Sağ tıklama menüsü
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Başlık Düzenle", command=self.rename_note)

    def open_book(self):
        file_path = filedialog.askopenfilename(filetypes=[("E-Kitap Dosyaları", "*.pdf *.epub")])
        if file_path:
            content = self.book_manager.read_book(file_path)
            self.text_area.config(state=tk.NORMAL)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, content)
            self.text_area.config(state=tk.DISABLED)

    def save_note(self):
        note = self.note_text_area.get("1.0", tk.END).strip()
        if note:
            self.note_manager.save_note(note)
            messagebox.showinfo("Bilgi", "Not başarıyla kaydedildi!")
            self.update_notes_list()
            self.note_text_area.delete(1.0, tk.END)  # Not kaydedildikten sonra not alanını temizle
        else:
            messagebox.showwarning("Uyarı", "Boş not kaydedilemez!")

    def update_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        notes = self.note_manager.load_notes()
        for i, note in enumerate(notes):
            self.notes_listbox.insert(tk.END, f"{i}: {note['timestamp']}")

    def delete_selected_note(self):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            self.note_manager.delete_note_by_index(index)
            self.update_notes_list()
            self.note_text_area.delete(1.0, tk.END)
            messagebox.showinfo("Bilgi", "Seçili not başarıyla silindi!")
        else:
            messagebox.showwarning("Uyarı", "Silmek için bir not seçin!")

    def rename_note(self):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            new_title = simpledialog.askstring("Başlık Değiştir", "Yeni başlık girin:")
            if new_title:
                self.note_manager.update_note_title(index, new_title)
                self.update_notes_list()

    def show_selected_note(self, event):
        selection = self.notes_listbox.curselection()
        if selection:
            index = selection[0]
            notes = self.note_manager.load_notes()
            note = notes[index]
            self.note_text_area.config(state=tk.NORMAL)
            self.note_text_area.delete(1.0, tk.END)
            self.note_text_area.insert(tk.END, note['content'])
            self.note_text_area.config(state=tk.DISABLED)

    def show_context_menu(self, event):
        try:
            self.context_menu.post(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1000x800")
    app = EBookReaderApp(root)
    root.mainloop()
