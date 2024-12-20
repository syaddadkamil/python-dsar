import streamlit as st
from database import simpan_struk  # Mengimpor fungsi dari database.py

def kasir_app():
    st.title("WARUNG NASI SEPIRING BAHAGIA")
    st.markdown("---")

    # Input nama pembeli
    st.header("Input Data Pembeli")
    pembeli = st.text_input("Nama pembeli:")
    if not pembeli.strip():
        pembeli = "Tidak Diketahui"
    st.write(f"Nama pembeli: {pembeli}")
    st.markdown("---")

    # Fungsi untuk memilih makanan
    def makanan():
        st.subheader("Menu Makanan")
        menu_makanan = {
            1: ("nasi uduk", 10000, "img/NASI-UDUK.jpe"),  
            2: ("nasi pecel", 15000, "img/NASI-PECEL.jpg"),  
            3: ("nasi campur", 15000, "img/NASI-CAMPUR.jpg"),  
            4: ("roti bakar", 5000, "img/ROTI-BAKAR.jpg"),  
            5: ("kentang", 5000, "img/KENTANG.jpg")  
        }

        pilihan_makanan = st.selectbox("Pilih makanan:", options=["nasi uduk", "nasi pecel", "nasi campur", "roti bakar", "kentang"])
        porsi = st.number_input("Berapa porsi?", min_value=1, value=1)

        for key, value in menu_makanan.items():
            if value[0] == pilihan_makanan:
                st.image(value[2], caption=value[0], use_container_width=True)  
                total_makanan = porsi * value[1]
                st.write(f"{porsi} {pilihan_makanan} = Rp.{total_makanan}")
                return total_makanan, pilihan_makanan, porsi

        return 0, "", 0  # Default return jika tidak ada pilihan yang valid

    # Fungsi untuk memilih minuman
    def minuman():
        st.subheader("Menu Minuman")
        menu_minuman = {
            1: ("es jeruk", 5000, "img/ES-JERUK.jpg"),  
            2: ("sop durian", 15000, "img/SOP-DURIAN.jpg"),  
            3: ("es campur", 10000, "img/ES-CAMPUR.jpg"),  
            4: ("matcha latte", 15000, "img/MATCHA-LATTE.jpg"),  
            5: ("cappuccino", 20000, "img/CAPPUCINO.jpg")  
        }

        pilihan_minuman = st.selectbox("Pilih minuman:", options=["es jeruk", "sop durian", "es campur", "matcha latte", "cappuccino"])
        gelas = st.number_input("Berapa gelas?", min_value=1, value=1)

        for key, value in menu_minuman.items():
            if value[0] == pilihan_minuman:
                st.image(value[2], caption=value[0], use_container_width=True)  
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
    st.markdown("---")
    st.subheader("Total Harga")
    st.write(f"Total Harga: Rp.{total_semua}")

    # Input pembayaran
    st.markdown("---")
    st.subheader("Pembayaran")
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
            st.success("Transaksi berhasil disimpan!")
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

            # Simpan ke database
            simpan_struk(
                pembeli,
                makanan_terpilih,
                porsi,
                total_makanan,
                minuman_terpilih,
                gelas,
                total_minuman,
                total_semua,
                kembalian
            )
