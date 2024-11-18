import sqlite3

from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

#
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS nilai_siswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nama_siswa TEXT,
        biologi INTEGER,
        fisika INTEGER,
        inggris INTEGER,
        predikisi_fakultas TEXT
    )
''')
    conn.commit()

def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM nilai_siswa')
    rows = cursor.fetchall()
    conn.close()
    return rows

def save_to_database(nama_siswa, biologi, fisika, inggris, predikisi_fakultas):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, predikisi_fakultas)
    VALUES (?, ?, ?, ?, ?)
    ''', (nama_siswa, biologi, fisika, inggris, predikisi_fakultas))
    conn.commit()
    conn.close()    



def update_database(record_id, nama, biologi, fisika, inggris, predikisi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('''
           UPDATE nilai_siswa
           SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, predikisi_fakultas = ?
           WHERE id = ?
    ''', (nama, biologi, fisika, inggris, predikisi, record_id))
    conn.commit()
    conn.close()

def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

def calculate_predikisi(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"
    
def submit():
    try:
        nama_siswa = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())
        
        if not nama_siswa:
            raise Exception("Nama Siswa tidak boleh kosong")
        
        predikisi = calculate_predikisi(biologi, fisika, inggris)
        save_to_database(nama_siswa, biologi, fisika, inggris, predikisi)

        messagebox.showinfo("Success", f"Data berhasil disimpan\nPredikisi Fakultas: {predikisi}")
        clear_inputs()
        populate_table()
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {str(e)}")

def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk diupdate")
        
        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise Exception("Nama Siswa tidak boleh kosong")
        
        predikisi = calculate_predikisi(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, predikisi)

        messagebox.showinfo("Success", f"Data berhasil diupdate\nPredikisi Fakultas: {predikisi}")
        clear_inputs()
        populate_table()
    except Exception as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus")
        
        record_id = int(selected_record_id.get())
        delete_database(record_id)

        messagebox.showinfo("Success", "Data berhasil dihapus")
        clear_inputs()
        populate_table()
    except ValueError as e:
        messagebox.showerror("Error", f"Kesalahan: {e}")

def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

def populate_table():
    for row  in tree.get_children():
        tree.delete(row)
    for row in fetch_data():
        tree.insert("", "end", values=row)

def fill_inputs_from_table(event):
    try:
        selected_item = tree.selection()[0]
        selected_row = tree.item(selected_item)['values']
        
        selected_record_id.set(selected_row[0])
        nama_var.set(selected_row[1])
        biologi_var.set(selected_row[2])
        fisika_var.set(selected_row[3])
        inggris_var.set(selected_row[4])
    except IndexError:
        messagebox.showerror("Error", "Pilih data yang valid!")

create_database()

root = Tk()
root.title("Aplikasi Nilai Siswa")

nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

Label(root, text="Nama Siswa").grid(row=0, column=0, padx=10, pady=5, sticky='w')
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Biologi").grid(row=1, column=0, padx=10, pady=5, sticky='w')
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Fisika").grid(row=2, column=0, padx=10, pady=5, sticky='w')
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Inggris").grid(row=3, column=0, padx=10, pady=5, sticky='w')
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

# Membuat tombol submit
Button(root, text="Submit", command=submit).grid(row=4, column=0, padx=10, pady=10)
# Membuat tombol update
Button(root, text="Update", command=update).grid(row=4, column=1, padx=10, pady=10)
# Membuat tombol delete
Button(root, text="Delete", command=delete).grid(row=4, column=2, padx=10, pady=10)

# Membuat Treeview untuk menampilkan data
tree = ttk.Treeview(root, columns=("ID", "Nama Siswa", "Biologi", "Fisika", "Inggris", "Prediksi Fakultas"), show='headings')
tree.heading("ID", text="ID")
tree.heading("Nama Siswa", text="Nama Siswa")
tree.heading("Biologi", text="Biologi")
tree.heading("Fisika", text="Fisika")
tree.heading("Inggris", text="Inggris")
tree.heading("Prediksi Fakultas", text="Prediksi Fakultas")
tree.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

# Menghubungkan event klik pada Treeview dengan fungsi
tree.bind("<ButtonRelease-1>", fill_inputs_from_table)

root.mainloop()




