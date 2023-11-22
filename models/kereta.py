class Kereta:
    def __init__(self, nama, jam_berangkat, jam_tiba, jumlah_kursi, harga, stasiun_awal, stasiun_tujuan):
        self.nama = nama
        self.jam_berangkat = jam_berangkat
        self.jam_tiba = jam_tiba
        self.jumlah_kursi = jumlah_kursi
        self.harga = harga
        self.stasiun_awal = stasiun_awal
        self.stasiun_tujuan = stasiun_tujuan
        self.kursi_terpilih = set()
