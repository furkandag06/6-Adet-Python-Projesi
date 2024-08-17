import qrcode
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser, ttk
import io
import pyperclip

def generate_qr_code(data, fill_color="black", back_color="white", box_size=10, border=4, version=1):
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=box_size,
        border=border
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color=fill_color, back_color=back_color)
    return img

def save_qr_code(img):
    file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG files", "*.png"), 
                                                        ("JPEG files", "*.jpg"), 
                                                        ("BMP files", "*.bmp"), 
                                                        ("All files", "*.*")])
    if file_path:
        img.save(file_path)
        messagebox.showinfo("Success", f"QR code saved as {file_path}")

def copy_qr_code():
    qr_img = save_button.image
    with io.BytesIO() as output:
        qr_img.save(output, format="PNG")
        img_data = output.getvalue()
    pyperclip.copy(img_data)
    messagebox.showinfo("Copied", "QR code copied to clipboard!")

def show_qr_code():
    data = entry.get()
    if not data:
        messagebox.showwarning("Input Error", "Please enter text or URL")
        return
    
    version = int(version_var.get())
    box_size = int(box_size_var.get())
    border = int(border_var.get())
    
    qr_img = generate_qr_code(data, fill_color=fill_color_var.get(), back_color=back_color_var.get(), box_size=box_size, border=border, version=version)
    
    qr_img_tk = ImageTk.PhotoImage(qr_img)
    label_img.config(image=qr_img_tk)
    label_img.image = qr_img_tk
    
    save_button.config(state=tk.NORMAL)
    copy_button.config(state=tk.NORMAL)
    print_button.config(state=tk.NORMAL)
    save_button.image = qr_img

def save_qr_code_button():
    img = save_button.image
    save_qr_code(img)

def print_qr_code():
    temp_file = "temp_qr_code.png"
    save_qr_code(temp_file)
    # Assuming you're using Windows; for other systems, consider other methods
    import win32api
    win32api.ShellExecute(0, "print", temp_file, None, ".", 0)

def choose_fill_color():
    color = colorchooser.askcolor()[1]
    if color:
        fill_color_var.set(color)
        fill_color_button.config(bg=color)

def choose_back_color():
    color = colorchooser.askcolor()[1]
    if color:
        back_color_var.set(color)
        back_color_button.config(bg=color)

def on_mouse_wheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

app = tk.Tk()
app.title("QR Code Generator")
app.geometry("500x350")  # Adjusted size
app.configure(bg="white")  # White background for the main window

style = ttk.Style()
style.configure('TButton',
                font=('Arial', 10, 'bold'),
                padding=6,
                relief="flat",
                background="white",
                foreground="black")
style.configure('TLabel', font=('Arial', 10), background="white", foreground="black")
style.configure('TEntry', padding=4, background="white", foreground="black")
style.map('TButton', background=[('active', '#e0e0e0')])

main_frame = ttk.Frame(app, padding=10, style='TFrame')
main_frame.pack(fill=tk.BOTH, expand=True)

# Create a canvas and a scrollbar for scrolling
canvas = tk.Canvas(main_frame)
scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
scrollable_frame = ttk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

# Bind the mouse wheel event to the canvas
app.bind_all("<MouseWheel>", on_mouse_wheel)

# QR Code Display Area
qr_display_frame = tk.Frame(scrollable_frame, bg="lightgray", width=300, height=300)
qr_display_frame.pack(pady=10, fill=tk.X)
qr_display_frame.grid_propagate(False)  # Prevent resizing

label_img = tk.Label(qr_display_frame, text=" QrCode Oluştur'a Basınca QR Codenuz Burada Oluşturalacaktır.", bg="lightgray")
label_img.pack(fill=tk.BOTH, expand=True)

input_frame = ttk.Frame(scrollable_frame)
input_frame.pack(pady=10)

ttk.Label(input_frame, text="Yazı veya URL Giriniz: ").grid(row=0, column=0, padx=5)
entry = ttk.Entry(input_frame, width=30)
entry.grid(row=0, column=1, padx=5)

# Adding buttons to the input frame
generate_button = ttk.Button(input_frame, text="QR Code Oluştur", command=show_qr_code)
generate_button.grid(row=1, column=0, padx=5, pady=5, columnspan=2, sticky='ew')

# Adding Save and Copy buttons side by side
button_frame = ttk.Frame(scrollable_frame)
button_frame.pack(pady=10)

save_button = ttk.Button(button_frame, text="QR Code'u Kaydet", state=tk.DISABLED, command=save_qr_code_button)
save_button.grid(row=0, column=0, padx=5)

copy_button = ttk.Button(button_frame, text="QR Code'u Kopyala", state=tk.DISABLED, command=copy_qr_code)
copy_button.grid(row=0, column=1, padx=5)

print_button = ttk.Button(button_frame, text="QR Code'u Yazdır", state=tk.DISABLED, command=print_qr_code)
print_button.grid(row=0, column=2, padx=5)

color_frame = ttk.Frame(scrollable_frame)
color_frame.pack(pady=10)

fill_color_var = tk.StringVar(value="#000000")  # Black
back_color_var = tk.StringVar(value="#ffffff")  # White

fill_color_button = ttk.Button(color_frame, text=" Ön Kısım Rengi Seç", command=choose_fill_color)
fill_color_button.grid(row=0, column=0, padx=10)

back_color_button = ttk.Button(color_frame, text="Arka Plan Rengi Seç", command=choose_back_color)
back_color_button.grid(row=0, column=1, padx=10)

options_frame = ttk.Frame(scrollable_frame)
options_frame.pack(pady=10)

ttk.Label(options_frame, text="Büyüklük:").grid(row=0, column=0, padx=5, sticky=tk.W)
box_size_var = tk.StringVar(value="10")
box_size_entry = ttk.Entry(options_frame, textvariable=box_size_var, width=5)
box_size_entry.grid(row=0, column=1, padx=5)

ttk.Label(options_frame, text="Sınır:").grid(row=0, column=2, padx=5, sticky=tk.W)
border_var = tk.StringVar(value="4")
border_entry = ttk.Entry(options_frame, textvariable=border_var, width=5)
border_entry.grid(row=0, column=3, padx=5)

ttk.Label(options_frame, text="Versiyon:").grid(row=0, column=4, padx=5, sticky=tk.W)
version_var = tk.StringVar(value="1")
version_entry = ttk.Entry(options_frame, textvariable=version_var, width=5)
version_entry.grid(row=0, column=5, padx=5)

app.mainloop()
