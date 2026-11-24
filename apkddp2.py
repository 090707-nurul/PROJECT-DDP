import streamlit as st

# ==========================================
# PENGATURAN HALAMAN APLIKASI (Tampilan Lebar)
# ==========================================
st.set_page_config(page_title="Aplikasi Manajemen KAS", layout="wide")

# ==========================================
# DESAIN WARNA TERANG - TEKS TETAP ITEM, GAK NYARU
# ==========================================
st.markdown("""
<style>
    /* Background utama - Kuning muda terang */
    .stApp {
        background-color: #FFF9E6;
    }
    /* Semua judul & teks utama jadi item pekat */
    .stApp h1, .stApp h2, .stApp h3 {
        color: #1A1A1A !important;
    }
    .stApp p, .stApp label, .stApp span {
        color: #1A1A1A;
    }

    /* Sidebar - Putih bersih */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 3px solid #FFD93D;
    }
    [data-testid="stSidebar"] h1 {
        color: #1A1A1A !important;
    }
    [data-testid="stSidebar"] p {
        color: #333333 !important;
    }
    /* Menu radio - teks item tebel */
    [data-testid="stSidebar"] label p {
        color: #1A1A1A !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }

    /* Kartu Metrik - Putih + border kuning */
    [data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 2px solid #FFD93D;
        border-radius: 16px;
        padding: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    }

    /* Tombol - Orange terang, teks putih */
    .stButton > button {
        background-color: #FF6B35 !important;
        color: white !important;
        border-radius: 12px;
        border: none;
        font-weight: 800;
        font-size: 16px;
        box-shadow: 0 4px 0 #D94F1F;
    }
    .stButton > button p {
        color: white !important;
    }

    /* Input - Putih, teks item */
    .stTextInput input, .stNumberInput input {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
    }

    /* Tabel - Putih */
    [data-testid="stTable"] {
        background-color: #FFFFFF;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 1. FUNGSI BUATAN SENDIRI (Tanpa OOP)
# ==========================================
TARGET_IURAN = 50000  # Target kas wajib per bulan (Rp 50.000)

def cek_status_bayar(nominal, target):
    if nominal >= target:
        return "Lunas"
    else:
        return "Belum Lunas"

def hitung_total_kas(daftar_transaksi):
    total = 0
    for item in daftar_transaksi:
        total = total + item["nominal"]
    return total

def hitung_jumlah_status(daftar_transaksi, status_dicari):
    jumlah = 0
    for item in daftar_transaksi:
        if item["status"] == status_dicari:
            jumlah = jumlah + 1
    return jumlah

# ==========================================
# 2. PENYIMPANAN DATA ANTAR-HALAMAN
# ==========================================
if "data_kas" not in st.session_state:
    st.session_state["data_kas"] = [
        {"nama": "Andi Pratama", "bulan": "Januari", "metode": "Transfer Bank", "nominal": 50000, "status": "Lunas"},
        {"nama": "Budi Santoso", "bulan": "Januari", "metode": "Tunai", "nominal": 25000, "status": "Belum Lunas"},
        {"nama": "Citra Lestari", "bulan": "Januari", "metode": "E-Wallet", "nominal": 50000, "status": "Lunas"},
        {"nama": "Dimas Saputra", "bulan": "Februari", "metode": "Tunai", "nominal": 30000, "status": "Belum Lunas"}
    ]

# ==========================================
# 3. NAVIGASI SIDEBAR (Seperti Menu Aplikasi)
# ==========================================
st.sidebar.title("KAS DIGITAL")
st.sidebar.markdown("Sistem Pencatatan Keuangan Kelas & Organisasi")
st.sidebar.markdown("---")

menu_aktif = st.sidebar.radio(
    "MENU UTAMA",
    [
        "Beranda",
        "Input Pembayaran",
        "Status Pembayaran",
        "Total KAS"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(f"Iuran Wajib: Rp {TARGET_IURAN:,} / bulan")

# ==========================================
# HALAMAN 1: BERANDA (Dashboard Utama)
# ==========================================
if menu_aktif == "Beranda":
    st.title("Beranda Aplikasi KAS")
    st.markdown("Selamat datang di pusat kendali pencatatan uang kas. Gunakan menu di samping kiri untuk mengelola transaksi.")

    semua_data = st.session_state["data_kas"]
    total_saldo = hitung_total_kas(semua_data)
    total_lunas = hitung_jumlah_status(semua_data, "Lunas")
    total_belum = hitung_jumlah_status(semua_data, "Belum Lunas")

    kol1, kol2, kol3 = st.columns(3)
    with kol1:
        st.metric("Total Saldo KAS", f"Rp {total_saldo:,}")
    with kol2:
        st.metric("Transaksi Lunas", f"{total_lunas} Orang")
    with kol3:
        st.metric("Belum Lunas", f"{total_belum} Orang")

    st.markdown("---")

    st.subheader("Fitur Utama Aplikasi")
    fitur1, fitur2, fitur3 = st.columns(3)
    with fitur1:
        st.info("**1. Input Pembayaran**\n\nCatat setoran kas anggota baru lengkap dengan pilihan bulan dan metode pembayaran.")
    with fitur2:
        st.success("**2. Status Pembayaran**\n\nPantau daftar anggota yang sudah lunas maupun yang masih memiliki tunggakan iuran.")
    with fitur3:
        st.warning("**3. Total KAS**\n\nLihat laporan akumulasi dana terkumpul, sisa kekurangan, serta grafik perbandingan kas.")

    st.subheader("Riwayat Transaksi Terbaru")
    st.table(semua_data)

# ==========================================
# HALAMAN 2: INPUT PEMBAYARAN
# ==========================================
elif menu_aktif == "Input Pembayaran":
    st.title("Input Pembayaran KAS")
    st.markdown("Masukkan rincian setoran uang kas anggota pada formulir di bawah ini.")

    kol_kiri, kol_kanan = st.columns(2)
    with kol_kiri:
        nama = st.text_input("Nama Lengkap Anggota", placeholder="Contoh: Rina Kartika")
        bulan = st.selectbox("Bulan Tagihan", ["Januari", "Februari", "Maret", "April", "Mei", "Juni"])
    with kol_kanan:
        metode = st.selectbox("Metode Pembayaran", ["Tunai", "Transfer Bank", "E-Wallet (QRIS)"])
        nominal = st.number_input(
            "Nominal Setoran (Rp)",
            min_value=0,
            max_value=1000000,
            value=50000,
            step=5000
        )

    if st.button("Simpan Pembayaran"):
        if nama.strip() == "":
            st.error("Gagal menyimpan: Nama anggota wajib diisi.")
        elif nominal <= 0:
            st.warning("Gagal menyimpan: Nominal setoran harus lebih besar dari Rp 0.")
        else:
            status_hasil = cek_status_bayar(nominal, TARGET_IURAN)
            transaksi_baru = {
                "nama": nama.strip(),
                "bulan": bulan,
                "metode": metode,
                "nominal": nominal,
                "status": status_hasil
            }
            st.session_state["data_kas"].append(transaksi_baru)

            if status_hasil == "Lunas":
                st.success(f"Berhasil! Pembayaran **{nama}** sebesar **Rp {nominal:,}** ({metode}) tercatat **Lunas**.")
            else:
                sisa_kurang = TARGET_IURAN - nominal
                st.warning(f"Tersimpan! Pembayaran **{nama}** berstatus **Belum Lunas** (Kurang Rp {sisa_kurang:,}).")

# ==========================================
# HALAMAN 3: STATUS PEMBAYARAN
# ==========================================
elif menu_aktif == "Status Pembayaran":
    st.title("Status Pembayaran Anggota")
    st.markdown("Filter dan cari status pelunasan kas setiap anggota.")

    kol_filter, kol_cari = st.columns(2)
    with kol_filter:
        pilih_status = st.radio("Filter Status", ["Semua", "Lunas", "Belum Lunas"], horizontal=True)
    with kol_cari:
        kata_kunci = st.text_input("Cari Nama Anggota", placeholder="Ketik nama untuk mencari...")

    hasil_filter = []
    for item in st.session_state["data_kas"]:
        cocok_status = (pilih_status == "Semua") or (item["status"] == pilih_status)
        cocok_nama = kata_kunci.lower() in item["nama"].lower()

        if cocok_status and cocok_nama:
            hasil_filter.append({
                "Nama Anggota": item["nama"],
                "Bulan": item["bulan"],
                "Metode": item["metode"],
                "Nominal (Rp)": item["nominal"],
                "Status": item["status"]
            })

    st.write(f"Menampilkan **{len(hasil_filter)}** data transaksi:")

    if len(hasil_filter) > 0:
        st.table(hasil_filter)
    else:
        st.warning("Tidak ada data pembayaran yang sesuai dengan filter pencarian.")

# ==========================================
# HALAMAN 4: TOTAL KAS
# ==========================================
elif menu_aktif == "Total KAS":
    st.title("Laporan & Total KAS")
    st.markdown("Rekapitulasi menyeluruh saldo kas terkumpul dan visualisasi grafik setoran.")

    semua_data = st.session_state["data_kas"]
    total_terkumpul = hitung_total_kas(semua_data)
    target_total = len(semua_data) * TARGET_IURAN
    kekurangan = max(0, target_total - total_terkumpul)

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total KAS Terkumpul", f"Rp {total_terkumpul:,}")
    with m2:
        st.metric("Target Seharusnya", f"Rp {target_total:,}")
    with m3:
        st.metric("Total Tunggakan", f"Rp {kekurangan:,}")

    if kekurangan == 0:
        st.success("Semua tagihan anggota yang tercatat sudah lunas sepenuhnya.")
    else:
        st.warning(f"Terdapat kekurangan kas sebesar **Rp {kekurangan:,}** dari anggota yang belum lunas.")

    st.markdown("---")

    grafik_kiri, grafik_kanan = st.columns(2)

    nama_anggota = []
    nominal_setoran = []
    akumulasi_saldo = []
    saldo_berjalan = 0

    for item in semua_data:
        nama_anggota.append(item["nama"])
        nominal_setoran.append(item["nominal"])
        saldo_berjalan = saldo_berjalan + item["nominal"]
        akumulasi_saldo.append(saldo_berjalan)

    with grafik_kiri:
        st.subheader("Grafik Setoran per Anggota")
        data_bar = {"Anggota": nama_anggota, "Nominal": nominal_setoran}
        st.bar_chart(data_bar, x="Anggota", y="Nominal")

    with grafik_kanan:
        st.subheader("Grafik Pertumbuhan Saldo KAS")
        st.line_chart(akumulasi_saldo)