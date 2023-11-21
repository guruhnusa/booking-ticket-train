import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import qrcode
from PIL import Image, ImageTk
import numpy as np
from models.stasiun import Stasiun
from models.kereta import Kereta
from models.user import User, UserManager 

class TicketBookingApp: 
    def __init__(self, root):
        self.root = root
        self.user_manager = UserManager()
        self.user_manager.load_from_csv()
        self.kursi_terpilih = [] 
        self.nama_penumpang_list = []
        self.tanggal_pesanan_var = None
        self.tanggal_pesanan = ""

        # Create the Tkinter root window
        self.root.title("Pemesanan Tiket Kereta")
        self.tampilkan_welcome_screen()
    
    def tampilkan_welcome_screen(self):
        tk.Label(self.root, text="Selamat Datang di Aplikasi Pemesanan Tiket Kereta", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        tk.Button(self.root, text="Start", command=self.tampilkan_halaman_login).grid(row=1, column=0, columnspan=2, pady=10)
    
    def tampilkan_halaman_login(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(self.root, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(self.root, text="Login", command=self.login).grid(row=2, column=0, pady=10)
        tk.Button(self.root, text="Daftar", command=self.buka_halaman_daftar).grid(row=2, column=1, pady=10)

        
    def login(self):
        
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.user_manager.check_credentials(username, password):
            self.tampilkan_halaman_pemesanan()
        else:
            messagebox.showwarning("Login Gagal", "Username atau password salah. Silakan coba lagi.")
            

    def buka_halaman_daftar(self):
        # Create a new window for registration
        jendela_daftar = tk.Toplevel(self.root)
        jendela_daftar.title("Pendaftaran")

        tk.Label(jendela_daftar, text="Username:").grid(row=0, column=0, padx=10, pady=10)
        username_entry = tk.Entry(jendela_daftar)
        username_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(jendela_daftar, text="Password:").grid(row=1, column=0, padx=10, pady=10)
        password_entry = tk.Entry(jendela_daftar, show="*")
        password_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Button(jendela_daftar, text="Daftar", command=lambda: self.daftar(jendela_daftar, username_entry.get(), password_entry.get())).grid(row=2, column=0, columnspan=2, pady=10)

    def daftar(self, jendela_daftar, username, password):
        if not username or not password:
            messagebox.showwarning("Peringatan", "Mohon isi semua kolom.")
            return

        # Check if the username already exists
        for user in self.user_manager.users:
            if user.username == username:
                messagebox.showwarning("Peringatan", "Username sudah digunakan. Silakan pilih username lain.")
                return

        # Register the new user
        new_user = User(username, password)
        self.user_manager.register_user(new_user)

        messagebox.showinfo("Pendaftaran Berhasil", "Akun berhasil didaftarkan. Silakan login.")
        # Close the registration window
        jendela_daftar.destroy()

        # Open the login window
        self.tampilkan_halaman_login()
    
    def tampilkan_halaman_pemesanan(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        # List objek Stasiun
        self.stasiun_list = [
            Stasiun("Gambir", "Jakarta"),
            Stasiun("Bandung", "Bandung"),
            Stasiun("Surabaya", "Surabaya"),
        ]

        # Variabel String untuk menyimpan stasiun awal dan tujuan
        self.stasiun_awal_var = tk.StringVar()
        self.stasiun_tujuan_var = tk.StringVar()

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

        self.tanggal_pesanan = self.tanggal_entry.get()  # Simpan tanggal yang dipilih

        # Menutup jendela utama
        self.root.withdraw()

        # Membuka jendela baru untuk halaman pemilihan kereta
        self.buka_jendela_kereta(stasiun_awal, stasiun_tujuan, self.tanggal_pesanan, jumlah_penumpang)

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
        jendela_kereta = tk.Toplevel(self.root)
        jendela_kereta.title("Pemilihan Kereta")

        # List objek Kereta
        self.kereta_list = [
            Kereta("Argo Bromo", "08:00", "12:00", 40, 200000),
            Kereta("Gajayana", "10:00", "14:00", 42, 150000),
            Kereta("Majapahit", "12:00", "16:00", 44, 100000),
            # Tambahkan kereta lain sesuai kebutuhan
        ]

        # Variabel untuk menyimpan pilihan kereta
        self.pilihan_kereta_var = tk.StringVar(value=self.kereta_list[0].nama)

        # Menampilkan informasi kereta, jam berangkat, dan jam tiba beserta radio button
        for i, kereta in enumerate(self.kereta_list):
            tk.Radiobutton(jendela_kereta, text=f"{kereta.nama} ({kereta.jumlah_kursi} kursi) - Harga: {kereta.harga}", variable=self.pilihan_kereta_var, value=kereta.nama).grid(row=i, column=0, columnspan=3, padx=10, pady=10)
            tk.Label(jendela_kereta, text=f"Jam Berangkat: {kereta.jam_berangkat}").grid(row=i, column=3, padx=10, pady=10)
            tk.Label(jendela_kereta, text=f"Jam Tiba: {kereta.jam_tiba}").grid(row=i, column=4, padx=10, pady=10)

        # Tombol Konfirmasi
        tk.Button(jendela_kereta, text="Konfirmasi", command=lambda: self.buka_halaman_kursi(jendela_kereta)).grid(row=len(self.kereta_list), column=0, columnspan=5, pady=10)

        jendela_kereta.mainloop()

    def buka_halaman_kursi(self, jendela_kereta):
        jendela_kereta.destroy()
        kereta_terpilih = next((kereta for kereta in self.kereta_list if kereta.nama == self.pilihan_kereta_var.get()), None)

        # Membuat jendela baru untuk halaman pemilihan kursi
        jendela_kursi = tk.Toplevel(self.root)  # Set the root window as the master
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

        tk.Button(jendela_kursi, text="Masukan Data Penumpang", command=lambda: self.buka_halaman_data_penumpang(jendela_kursi, kereta_terpilih)).grid(row=num_rows, column=0, columnspan=num_columns, pady=10)

        jendela_kursi.mainloop()

    def buka_halaman_data_penumpang(self, jendela_kursi, kereta_terpilih):
        jendela_kursi.destroy()  # Close the seat selection window
        jendela_data_penumpang = tk.Toplevel()
        jendela_data_penumpang.title("Isi Data Penumpang")

        # Label dan Entry untuk setiap penumpang
        for i in range(int(self.jumlah_penumpang_var.get())):
            tk.Label(jendela_data_penumpang, text=f"Nama Penumpang {i + 1}:").grid(row=i, column=0, padx=10, pady=10)
            entry_nama = tk.Entry(jendela_data_penumpang)
            entry_nama.grid(row=i, column=1, padx=10, pady=10)
            self.nama_penumpang_list.append(entry_nama)  # Tambahkan nama penumpang ke dalam list

        # Tombol Konfirmasi Data Penumpang
        tk.Button(jendela_data_penumpang, text="Konfirmasi", command=lambda: self.tampilkan_data_pesanan(jendela_data_penumpang, kereta_terpilih)).grid(row=int(self.jumlah_penumpang_var.get()), column=0, columnspan=2, pady=10)

        
    def tampilkan_data_pesanan(self, jendela_data_penumpang, kereta_terpilih):
        # Simpan data penumpang sebelum jendela dihancurkan
        data_penumpang = [entry_nama.get() for entry_nama in self.nama_penumpang_list]

        # Hancurkan jendela setelah menyimpan data penumpang
        jendela_data_penumpang.destroy()

        # Membuat jendela baru untuk menampilkan data pesanan
        jendela_data_pesanan = tk.Toplevel()
        jendela_data_pesanan.title("Data Pesanan")

        # Menampilkan data pesanan
        tk.Label(jendela_data_pesanan, text=f"Tanggal: {self.tanggal_pesanan}").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(jendela_data_pesanan, text=f"Kereta: {kereta_terpilih.nama}").grid(row=1, column=0, padx=10, pady=10)
       

        # Menampilkan nama-nama penumpang
        for i, nama in enumerate(data_penumpang):
            tk.Label(jendela_data_pesanan, text=f"Nama Penumpang {i + 1}: {nama}").grid(row=i + 2, column=0, padx=10, pady=10)

        total_harga = kereta_terpilih.harga * len(data_penumpang)
        tk.Label(jendela_data_pesanan, text=f"Total Harga: {total_harga}").grid(row=len(data_penumpang) + 2, column=0, padx=10, pady=10)

        # Tombol untuk membuka halaman pembayaran
        tk.Button(jendela_data_pesanan, text="Pembayaran", command=lambda: self.konfirmasi_pembayaran(jendela_data_pesanan, kereta_terpilih, data_penumpang, total_harga)).grid(row=len(data_penumpang) + 3, column=0, padx=10, pady=10)

        jendela_data_pesanan.mainloop()

    def konfirmasi_pesanan(self, jendela_kursi, kereta_terpilih):
        jendela_kursi.destroy()
        self.buka_halaman_data_penumpang(kereta_terpilih)
    
    def konfirmasi_pembayaran(self, jendela_data_pesanan, kereta_terpilih, data_penumpang, total_harga):
        # Close the data_pesanan window
        jendela_data_pesanan.destroy()

        # Membuat jendela baru untuk pembayaran
        jendela_pembayaran = tk.Toplevel()
        jendela_pembayaran.title("Pembayaran")

        # Menampilkan informasi pembayaran
        # Menampilkan informasi pembayaran
        tk.Label(jendela_pembayaran, text=f"Total Harga: {total_harga}", font=("Helvetica", 12)).pack(padx=10, pady=10)
        tk.Label(jendela_pembayaran, text="Scan Kode QR ini", font=("Helvetica", 12)).pack(padx=10, pady=10)


        # Generate QR code for the total price
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(str(total_harga))
        qr.make(fit=True)

        # Get the QR code image
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Convert the image to a Tkinter PhotoImage
        tk_image = ImageTk.PhotoImage(Image.fromarray(np.array(qr_image)))

        # Display the QR code
        tk.Label(jendela_pembayaran, image=tk_image).pack(padx=10, pady=10)

        tk.Button(jendela_pembayaran, text="Selesai", command=lambda: self.selesai_pembayaran()).pack(padx=10, pady=10)
        jendela_pembayaran.mainloop()
    
    def selesai_pembayaran(self):
        tk.messagebox.showinfo("Terima Kasih", "Terima kasih telah menggunakan layanan kami!")
        self.root.destroy()  # Close the main window after showing the message