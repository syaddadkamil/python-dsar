import streamlit as st
import pandas as pd
import os

# Menampilkan judul aplikasi
st.title("WARUNG NASI SEPIRING BAHAGIA")

# Input nama pembeli
pembeli = st.text_input("Nama pembeli:")
if not pembeli.strip():
    pembeli = "Tidak Diketahui"
st.write(f"Nama pembeli: {pembeli}")

# Fungsi untuk memilih makanan
def makanan():
    st.write("MENU MAKANAN")
    menu_makanan = {
        1: ("nasi uduk", 10000),
        2: ("nasi pecel", 15000),
        3: ("nasi campur", 15000)
    }

    # Pilihan makanan
    pilihan_makanan = st.selectbox("Pilih makanan:", options=["nasi uduk", "nasi pecel", "nasi campur"])
    porsi = st.number_input("Berapa porsi?", min_value=1, value=1)

    # Menghitung harga makanan
    for key, value in menu_makanan.items():
        if value[0] == pilihan_makanan:
            total_makanan = porsi * value[1]
            st.write(f"{porsi} {pilihan_makanan} = Rp.{total_makanan}")
            return total_makanan, pilihan_makanan, porsi

    return 0, "", 0  # Default return jika tidak ada pilihan yang valid

# Fungsi untuk memilih minuman
def minuman():
    st.write("MENU MINUMAN")
    menu_minuman = {
        1: ("es jeruk", 5000),
        2: ("sop durian", 15000),
        3: ("es campur", 10000)
    }

    # Pilihan minuman
    pilihan_minuman = st.selectbox("Pilih minuman:", options=["es jeruk", "sop durian", "es campur"])
    gelas = st.number_input("Berapa gelas?", min_value=1, value=1)

    # Menghitung harga minuman
    for key, value in menu_minuman.items():
        if value[0] == pilihan_minuman:
            total_minuman = gelas * value[1]
            st.write(f"{gelas} {pilihan_minuman} = Rp.{total_minuman}")
            return total_minuman, pilihan_minuman, gelas

    return 0, "", 0  # Default return jika tidak ada pilihan yang valid

# Memanggil fungsi makanan dan minuman
total_makanan, makanan_terpilih, porsi = makanan()
total_minuman, minuman_terpilih, gelas = minuman()

# Menghitung total semua
total_semua = total_makanan + total_minuman

# Menampilkan total harga setelah memilih menu
st.write(f"\nTotal Harga: Rp.{total_semua}")

# Input pembayaran
uang = st.number_input("Uang tunai pembeli:", min_value=1)

# Memastikan uang cukup untuk membayar
if uang >= total_semua:
    kembalian = uang - total_semua
else:
    kembalian = 0
    st.warning("Uang tunai kurang, silahkan masukkan jumlah yang cukup.")

# Tombol untuk menyimpan struk
if st.button("Simpan Struk"):
    if uang >= total_semua:
        st.write("S T R U K B E L I")
        st.write(f"Nama         : {pembeli}")
        if makanan_terpilih:
            st.write(f"Beli         : {porsi} {makanan_terpilih} (Rp.{total_makanan})")
        if minuman_terpilih:
            st.write(f"              {gelas} {minuman_terpilih} (Rp.{total_minuman})")
        st.write(f"Tagihan      : Rp.{total_semua}")
        st.write(f"Dibayar      : Rp.{uang}")
        st.write(f"Kembalian    : Rp.{kembalian}")
        st.write("\nTerima kasih telah berbelanja di WARUNG NASI SEPIRING BAHAGIA!")

        # Menyimpan struk ke file Excel
        file_name = "database_struk.xlsx"
        data = {
            "Nama Pembeli": [pembeli],
            "Makanan": [f"{porsi} {makanan_terpilih}" if makanan_terpilih else "-"],
            "Harga Makanan": [total_makanan],
            "Minuman": [f"{gelas} {minuman_terpilih}" if minuman_terpilih else "-"],
            "Harga Minuman": [total_minuman],
            "Total": [total_semua],
            "Uang Tunai": [uang],
            "Kembalian": [kembalian]
        }

        if os.path.exists(file_name):
            existing_data = pd.read_excel(file_name)
            new_data = pd.DataFrame(data)

            # Cek jika data sama sudah ada untuk mencegah duplikat
            if not existing_data.equals(pd.concat([existing_data, new_data], ignore_index=True)):
                updated_data = pd.concat([existing_data, new_data], ignore_index=True)
                updated_data.to_excel(file_name, index=False)
        else:
            pd.DataFrame(data).to_excel(file_name, index=False)

        st.success("Data transaksi telah disimpan ke database Excel.")

# Menambahkan fitur untuk melihat data
if st.button("Lihat Database Transaksi"):
    file_name = "database_struk.xlsx"
    if os.path.exists(file_name):
        df = pd.read_excel(file_name)
        st.write("Data Transaksi:")
        st.dataframe(df)
    else:
        st.warning("Database belum tersedia. Lakukan transaksi terlebih dahulu untuk membuat database.")
