class Kereta:
    def __init__(self, nama, jam_berangkat, jam_tiba, jumlah_kursi, harga):
        self.nama = nama
        self.jam_berangkat = jam_berangkat
        self.jam_tiba = jam_tiba
        self.jumlah_kursi = jumlah_kursi
        self.kursi_terpilih = set()
        self.harga = harga  # Menambahkan atribut harga