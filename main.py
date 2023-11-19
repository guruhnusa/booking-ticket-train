import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry

class Stasiun:
    def __init__(self, nama, kota):
        self.nama = nama
        self.kota = kota

class Kereta:
    def __init__(self, nama, jam_berangkat, jam_tiba, jumlah_kursi):
        self.nama = nama
        self.jam_berangkat = jam_berangkat
        self.jam_tiba = jam_tiba
        self.jumlah_kursi = jumlah_kursi
        self.kursi_terpilih = set()

class TicketBookingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pemesanan Tiket Kereta")
        self.tampilkan_halaman_pemesanan()

    def tampilkan_halaman_pemesanan(self):
        # List objek Stasiun
        self.stasiun_list = [
            Stasiun("Gambir", "Jakarta"),
            Stasiun("Bandung", "Bandung"),
            Stasiun("Surabaya", "Surabaya"),
            # Tambahkan stasiun lain sesuai kebutuhan
        ]

        # Variabel String untuk menyimpan stasiun awal dan tujuan
        self.stasiun_awal_var = tk.StringVar()
        self.stasiun_tujuan_var = tk.StringVar()

        # Variabel untuk menyimpan tanggal
        self.tanggal_var = tk.StringVar()

        # Variabel String untuk menyimpan jumlah penumpang
        self.jumlah_penumpang_var = tk.StringVar()

        # Label dan OptionMenu untuk Stasiun Awal
        tk.Label(self.root, text="Stasiun Awal:").grid(row=0, column=0, padx=10, pady=10)
        stasiun_awal_options = [stasiun.nama for stasiun in self.stasiun_list]
        tk.OptionMenu(self.root, self.stasiun_awal_var, *stasiun_awal_options).grid(row=0, column=1, padx=10, pady=10)

        # Label dan OptionMenu untuk Stasiun Tujuan
        tk.Label(self.root, text="Stasiun Tujuan:").grid(row=1, column=0, padx=10, pady=10)
        stasiun_tujuan_options = [stasiun.nama for stasiun in self.stasiun_list]
        tk.OptionMenu(self.root, self.stasiun_tujuan_var, *stasiun_tujuan_options).grid(row=1, column=1, padx=10, pady=10)

        # Label dan DateEntry untuk Tanggal
        tk.Label(self.root, text="Tanggal:").grid(row=2, column=0, padx=10, pady=10)
        self.tanggal_entry = DateEntry(self.root, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.tanggal_entry.grid(row=2, column=1, padx=10, pady=10)

        # Label dan Entry untuk Jumlah Penumpang
        tk.Label(self.root, text="Jumlah Penumpang (max 5):").grid(row=3, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.jumlah_penumpang_var).grid(row=3, column=1, padx=10, pady=10)

        # Tombol Pemesanan
        tk.Button(self.root, text="Pesan Tiket", command=self.buka_halaman_kereta).grid(row=4, column=0, columnspan=2, pady=10)

    def buka_halaman_kereta(self):
        stasiun_awal = self.stasiun_awal_var.get()
        stasiun_tujuan = self.stasiun_tujuan_var.get()
        tanggal = self.tanggal_entry.get()
        jumlah_penumpang = self.jumlah_penumpang_var.get()

        # Validasi input
        if not stasiun_awal or not stasiun_tujuan or not tanggal or not jumlah_penumpang:
            messagebox.showwarning("Peringatan", "Mohon isi semua kolom.")
            return

        # Validasi stasiun tujuan tidak sama dengan stasiun pemberangkatan
        if stasiun_awal == stasiun_tujuan:
            messagebox.showwarning("Peringatan", "Stasiun tujuan tidak boleh sama dengan stasiun pemberangkatan.")
            return

        # Validasi jumlah penumpang maksimal 5
        try:
            jumlah_penumpang = int(jumlah_penumpang)
            if jumlah_penumpang <= 0 or jumlah_penumpang > 5:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Peringatan", "Jumlah penumpang harus antara 1 dan 5.")
            return

        # Menutup jendela utama
        self.root.destroy()

        # Membuka jendela baru untuk halaman pemilihan kereta
        self.buka_jendela_kereta(stasiun_awal, stasiun_tujuan, tanggal, jumlah_penumpang)


    def buka_jendela_kereta(self, stasiun_awal, stasiun_tujuan, tanggal, jumlah_penumpang):
        # Membuat jendela baru untuk halaman pemilihan kereta
        jendela_kereta = tk.Tk()
        jendela_kereta.title("Pemilihan Kereta")

        # List objek Kereta
        self.kereta_list = [
            Kereta("Argo Bromo", "08:00", "12:00", 40),
            Kereta("Gajayana", "10:00", "14:00", 42),
            Kereta("Majapahit", "12:00", "16:00", 44),
            # Tambahkan kereta lain sesuai kebutuhan
        ]

        # Variabel untuk menyimpan pilihan kereta
        self.pilihan_kereta_var = tk.StringVar(value=self.kereta_list[0].nama)

        # Menampilkan informasi kereta, jam berangkat, dan jam tiba beserta radio button
        for i, kereta in enumerate(self.kereta_list):
            tk.Radiobutton(jendela_kereta, text=f"{kereta.nama} ({kereta.jumlah_kursi} kursi)", variable=self.pilihan_kereta_var, value=kereta.nama).grid(row=i, column=0, padx=10, pady=10)
            tk.Label(jendela_kereta, text=f"Jam Berangkat: {kereta.jam_berangkat}").grid(row=i, column=1, padx=10, pady=10)
            tk.Label(jendela_kereta, text=f"Jam Tiba: {kereta.jam_tiba}").grid(row=i, column=2, padx=10, pady=10)

        # Tombol Konfirmasi
        tk.Button(jendela_kereta, text="Konfirmasi", command=lambda: self.buka_halaman_kursi(jendela_kereta)).grid(row=len(self.kereta_list), column=0, columnspan=3, pady=10)

        jendela_kereta.mainloop()


    def buka_halaman_kursi(self, jendela_kereta):
        jendela_kereta.destroy()
        kereta_terpilih = next((kereta for kereta in self.kereta_list if kereta.nama == self.pilihan_kereta_var.get()), None)

        # Membuat jendela baru untuk halaman pemilihan kursi
        jendela_kursi = tk.Tk()
        jendela_kursi.title("Pemilihan Kursi")

        # Variabel untuk menyimpan kursi yang dipilih
        self.kursi_terpilih_vars = []

        # Fungsi yang dipanggil saat tombol kursi ditekan
        def on_kursi_button_click(index):
            var = self.kursi_terpilih_vars[index]
            button_kursi = buttons[index]

            # Check if the user has already selected the maximum number of seats
            max_seats = int(self.jumlah_penumpang_var.get())
            selected_seats = sum(1 for var in self.kursi_terpilih_vars if var.get() == "1")

            if selected_seats == max_seats:
                # Allow changing the selected seat
                if var.get() == "1":
                    button_kursi.configure(bg="SystemButtonFace")
                    var.set("0")
                else:
                    messagebox.showwarning("Peringatan", "Anda sudah memilih semua kursi yang diperlukan.")
            else:
                # Toggle the selection of the seat
                if var.get() == "0":
                    button_kursi.configure(bg="red")
                    var.set("1")
                else:
                    button_kursi.configure(bg="SystemButtonFace")
                    var.set("0")

        # Menampilkan tabel kursi beserta button
        num_rows = kereta_terpilih.jumlah_kursi // 4
        num_columns = 4

        buttons = []

        for i in range(num_rows):
            for j in range(num_columns):
                seat_label = chr(65 + i) + str(j + 1)
                if seat_label == 'A2':
                    seat_label = 'A2 '  # Add space for A2
                var = tk.StringVar(value="0")
                self.kursi_terpilih_vars.append(var)

                button_kursi = tk.Button(jendela_kursi, text=f"{seat_label}", command=lambda i=i, j=j: on_kursi_button_click(i * num_columns + j))
                button_kursi.grid(row=i, column=j, padx=10, pady=10)
                buttons.append(button_kursi)

        # Tombol Konfirmasi Kursi
        tk.Button(jendela_kursi, text="Konfirmasi", command=lambda: self.konfirmasi_pesanan(jendela_kursi, kereta_terpilih)).grid(row=num_rows, column=0, columnspan=num_columns, pady=10)

        jendela_kursi.mainloop()

    def konfirmasi_pesanan(self, jendela_kursi, kereta_terpilih):
        jendela_kursi.destroy()  # Tutup jendela pemilihan kursi
        # Mendapatkan kursi yang dipilih oleh pengguna
        kursi_terpilih = [i+1 for i, var in enumerate(self.kursi_terpilih_vars) if var.get() == "1"]

        # Validasi jumlah kursi yang dipilih sesuai dengan jumlah penumpang
        jumlah_penumpang = int(self.jumlah_penumpang_var.get())
        if len(kursi_terpilih) != jumlah_penumpang:
            messagebox.showwarning("Peringatan", "Jumlah kursi yang dipilih harus sesuai dengan jumlah penumpang.")
            return

        # Membuat jendela baru untuk memasukkan data penumpang
        jendela_data_penumpang = tk.Tk()
        jendela_data_penumpang.title("Data Penumpang")

        # List untuk menyimpan data penumpang
        data_penumpang = []

        # Fungsi untuk memproses data penumpang
        def simpan_data_penumpang(i):
            nama = entry_nama.get()
            nik = entry_nik.get()
            data_penumpang.append({"Nama": nama, "NIK": nik})

            # Bersihkan input fields
            entry_nama.delete(0, tk.END)
            entry_nik.delete(0, tk.END)

            # Fokus ke input nama untuk penumpang berikutnya
            entry_nama.focus()

            # Tampilkan pesan konfirmasi setelah memasukkan data penumpang terakhir
            if i == jumlah_penumpang - 1:
                self.konfirmasi_pesanan_lanjut(jendela_data_penumpang, kereta_terpilih, data_penumpang)

        # Menampilkan input fields untuk setiap penumpang
        for i in range(jumlah_penumpang):
            tk.Label(jendela_data_penumpang, text=f"Data Penumpang {i+1}").grid(row=i*3, column=0, columnspan=2, pady=10)
            tk.Label(jendela_data_penumpang, text="Nama:").grid(row=i*3 + 1, column=0, pady=5)
            tk.Label(jendela_data_penumpang, text="NIK:").grid(row=i*3 + 2, column=0, pady=5)

            entry_nama = tk.Entry(jendela_data_penumpang, font=('Arial', 14))  # Larger font size
            entry_nama.grid(row=i*3 + 1, column=1, pady=5)

            entry_nik = tk.Entry(jendela_data_penumpang, font=('Arial', 14))  # Larger font size
            entry_nik.grid(row=i*3 + 2, column=1, pady=5)

            # Set fokus ke input nama untuk penumpang pertama
            if i == 0:
                entry_nama.focus()

            # Tombol Konfirmasi Data Penumpang
            tk.Button(jendela_data_penumpang, text="Konfirmasi", command=lambda i=i: simpan_data_penumpang(i)).grid(row=jumlah_penumpang*3 + 1, column=0, columnspan=2, pady=10)

        jendela_data_penumpang.mainloop()


    # Method untuk melanjutkan proses setelah mengonfirmasi data penumpang
    def konfirmasi_pesanan_lanjut(self, jendela_data_penumpang, kereta_terpilih, data_penumpang):
        jendela_data_penumpang.destroy()  # Tutup jendela input data penumpang

        # Initialize kursi_terpilih with an empty list
        kursi_terpilih = []

        # Membuat jendela baru untuk menampilkan data pesanan
        jendela_data_pesanan = tk.Tk()
        jendela_data_pesanan.title("Data Pesanan")

        # Menampilkan informasi pesanan
        tk.Label(jendela_data_pesanan, text=f"Informasi Pesanan untuk Kereta {kereta_terpilih.nama}").grid(row=0, column=0, columnspan=2, pady=10)

        # Menampilkan data penumpang
        tk.Label(jendela_data_pesanan, text="Data Penumpang:").grid(row=1, column=0, columnspan=2, pady=5)
        for i, penumpang in enumerate(data_penumpang, start=2):
            tk.Label(jendela_data_pesanan, text=f"{i - 1}. Nama: {penumpang['Nama']}, NIK: {penumpang['NIK']}").grid(row=i, column=0, columnspan=2, pady=5)

        # Menampilkan kursi yang dipilih
        tk.Label(jendela_data_pesanan, text="Kursi yang Dipilih:").grid(row=i + 1, column=0, columnspan=2, pady=5)
        kursi_terpilih = [f"Kursi {chr(65 + (seat-1) // 4)}{(seat-1) % 4 + 1}" for seat in kursi_terpilih]
        tk.Label(jendela_data_pesanan, text=", ".join(kursi_terpilih)).grid(row=i + 2, column=0, columnspan=2, pady=5)

        # Tombol Selesai
        tk.Button(jendela_data_pesanan, text="Selesai", command=jendela_data_pesanan.destroy).grid(row=i + 3, column=0, columnspan=2, pady=10)

        jendela_data_pesanan.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = TicketBookingApp(root)
    root.mainloop()
