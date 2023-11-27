import tkinter as tk
from tkinter import simpledialog, messagebox
from tkcalendar import Calendar
from datetime import datetime

# UNTUK MENAMBAHKAN WARNA PADA LISTBOX TUGAS AKTIF
class ColorListbox(tk.Listbox):
    def __init__(self, master, **kwargs):
        tk.Listbox.__init__(self, master, **kwargs)

    def warna(self, color, *args, **kwargs):
        self.insert(*args, **kwargs)
        self.itemconfig(tk.END, {'foreground': color})

# MENAMBAHKAN TUGAS 
def get_tugas():
    tugas_text = simpledialog.askstring("Tambah Tugas", "Enter Tugas")
    if not tugas_text:
        messagebox.showwarning("Warning", "Silakan masukkan Tugas.")
    else:
        tugas_date = pick_date()
        if tugas_date:
            add_tugas(tugas_text, tugas_date)

# MEMILIH TANGGAL SEBELUM TUGAS DATE
def pick_date():
    top = tk.Toplevel()
    cal = Calendar(top, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
    cal.pack(padx=10, pady=10)
    
    def set_date():
        top.destroy()
        return cal.get_date()

    ok_button = tk.Button(top, text="OK", command=set_date)
    ok_button.pack(pady=10)
    top.wait_window()
    return cal.get_date()

# MENAMBAHKAN TUGAS AKTIF KE DALAM LISTBOX
def add_tugas(tugas_text, tugas_date):
    tugas_deadline = deadline_var.get()
    if tugas_date and tugas_deadline:
        try:
            current_time = datetime.now().strftime('(%H:%M:%S)')  
            tugas_date = datetime.strptime(tugas_date, '%m/%d/%y').strftime('%Y-%m-%d')
            tugas_date = datetime.strptime(tugas_date, '%Y-%m-%d').date()
            if tugas_deadline == 'Tidak Mendesak':
                aktif_listbox.warna('green', tk.END, f"{tugas_text} - {tugas_date} {current_time}")
            elif tugas_deadline == 'Mendesak':
                aktif_listbox.warna('orange', tk.END, f"{tugas_text} - {tugas_date} {current_time}")
            elif tugas_deadline == 'Sangat Mendesak':
                aktif_listbox.warna('red', tk.END, f"{tugas_text} - {tugas_date} {current_time}")
            elif tugas_deadline == 'Deadline':
                messagebox.showwarning("Warning", "Masukan pilihan deadline terlebih dahulu")
            save_data()
        except ValueError:
            messagebox.showwarning("Warning", "Masukan data yang benar")

# MENYELESAIKAN TUGAS
def selesai_tugas():
    selections = aktif_listbox.curselection()
    if selections:
        for selection in selections:
            item = aktif_listbox.get(selection)
            selesai_listbox.insert(tk.END, item)
        for i in reversed(selections):
            aktif_listbox.delete(i)
        save_data()

# MENGHAPUS TUGAS
def delete_tugas():
    selection = selesai_listbox.curselection()
    if selection:
        selesai_listbox.delete(selection)
        save_data()

# MENCARI TUGAS
def search_tugas():
    search_text = simpledialog.askstring("Cari Tugas", "Masukkan Tugas yang Dicari")
    if search_text:
        for index in range(aktif_listbox.size()):
            if search_text.lower() in aktif_listbox.get(index).lower():
                aktif_listbox.selection_clear(0, tk.END)
                aktif_listbox.selection_set(index)
                aktif_listbox.see(index)
                break
        else:
            messagebox.showwarning("Pencarian", f"Tugas '{search_text}' tidak ditemukan.")

# MENYIMPAN DATA KEDALAM FILE TXT
def save_data():
    try:
        with open('data.txt', 'w') as f:
            f.write("Tugas Aktif:\n")
            for index in range(aktif_listbox.size()):
                item = aktif_listbox.get(index)
                color = aktif_listbox.itemcget(index, 'foreground')
                f.write(f"{item},{color}\n")
            f.write("\nTugas Selesai:\n")
            for index in range(selesai_listbox.size()):
                item = selesai_listbox.get(index)
                color = selesai_listbox.itemcget(index, 'foreground')
                f.write(f"{item},{color}\n")
    except Exception as e:
        messagebox.showwarning("Warning", f"Gagal untuk menyimpan data: {e}")

# MENLOADING DATA KETIKA MASUK KEMBALI
def load_data():
    try:
        with open('data.txt', 'r') as f:
            lines = f.readlines()
            aktif_flag = False
            selesai_flag = False
            for line in lines:
                line = line.strip()
                if line == "Tugas Aktif:":
                    aktif_flag = True
                    selesai_flag = False
                elif line == "Tugas Selesai:":
                    aktif_flag = False
                    selesai_flag = True
                elif line and (aktif_flag or selesai_flag):
                    task, color = line.rsplit(',', 1)
                    if aktif_flag:
                        aktif_listbox.warna(color.strip(), tk.END, task)
                    elif selesai_flag:
                        selesai_listbox.warna(color.strip(), tk.END, task)
    except FileNotFoundError:
        messagebox.showwarning("Warning", f"Gagal untuk mencari data:")

# DESIGNING APLIKASI
app = tk.Tk()
app.title("Asisten Mahasiswa")
app.configure(bg='#3498db') 
app.resizable(False, False) 

cal = Calendar(app, selectmode='day', year=datetime.now().year, month=datetime.now().month, day=datetime.now().day)
cal.grid(row=0, column=0, columnspan=5, padx=10, pady=10, sticky='n')

deadline_var = tk.StringVar(app)
deadline_var.set("Deadline")
deadline_dropdown = tk.OptionMenu(app, deadline_var, "Tidak Mendesak", "Mendesak", "Sangat Mendesak")
deadline_dropdown.grid(row=1, column=0, columnspan=5, padx=10, pady=10, sticky='n')

add_button = tk.Button(app, text="Tambah Tugas", command=get_tugas)
add_button.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky='n')

search_button = tk.Button(app, text="Cari Tugas", command=search_tugas, bg='#FF5733', fg='#ffffff')
search_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky='w')

aktif_label = tk.Label(app, text="Tugas Aktif", font=('Arial', 14, 'bold'), bg='#3498db', fg='white')
aktif_label.grid(row=3, column=0, padx=10, pady=5, columnspan=2, sticky='n')

aktif_listbox = ColorListbox(app, width=40, height=10, bg='#ffffff', font=('Arial', 12))
aktif_listbox.grid(row=4, column=0, padx=10, pady=5, rowspan=4, columnspan=2, sticky='n')

selesai_button = tk.Button(app, text="Selesaikan Tugas", command=selesai_tugas, bg='#4CAF50', fg='#ffffff')
selesai_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10, sticky='e')

selesai_label = tk.Label(app, text="Tugas Selesai", font=('Arial', 14, 'bold'), bg='#3498db', fg='white')
selesai_label.grid(row=3, column=2, padx=10, pady=5, columnspan=3, sticky='n')

selesai_listbox = ColorListbox(app, width=40, height=10, bg='#ffffff', font=('Arial', 12))
selesai_listbox.grid(row=4, column=2, padx=10, pady=5, rowspan=4, columnspan=3, sticky='e')

delete_button = tk.Button(app, text="Hapus Tugas", command=delete_tugas, bg='#FF0000', fg='#ffffff')
delete_button.grid(row=8, column=2, padx=10, pady=10, sticky='w')

load_data()
app.mainloop()