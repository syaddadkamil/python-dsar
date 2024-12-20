import pandas as pd
import streamlit as st
from datetime import datetime

# Fungsi untuk menyimpan struk transaksi dalam format Excel
def simpan_struk(pembeli, makanan_terpilih, porsi, total_makanan, minuman_terpilih, gelas, total_minuman, total_semua, kembalian):
    import os
    tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    transaksi = {
        "Tanggal": [tanggal],
        "Nama Pembeli": [pembeli],
        "Pesanan Makanan": [f"{porsi}x {makanan_terpilih}" if makanan_terpilih else ""],
        "Pesanan Minuman": [f"{gelas}x {minuman_terpilih}" if minuman_terpilih else ""],
        "Harga Makanan": [total_makanan],
        "Harga Minuman": [total_minuman],
        "Total Harga": [total_semua],
        "Kembalian": [kembalian],
    }
    df = pd.DataFrame(transaksi)

    # Menyimpan data ke file Excel
    file_name = 'transaksi.xlsx'
    if not os.path.exists(file_name):  # Jika file tidak ada, buat file baru
        with pd.ExcelWriter(file_name, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Transaksi")
    else:  # Jika file ada, tambahkan data di bawahnya
        with pd.ExcelWriter(file_name, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=not writer.sheets, sheet_name="Transaksi", 
                        startrow=writer.sheets.get("Transaksi", 0).max_row if writer.sheets else 0)


# Fungsi untuk melihat isi database
def lihat_database():
    try:
        file_name = 'transaksi.xlsx'
        df = pd.read_excel(file_name, sheet_name="Transaksi")
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca database: {e}")
        return None

# Fungsi dashboard database
def database_app():
    st.title("Database Transaksi")
    df = lihat_database()
    if df is not None and not df.empty:
        st.write("Data Transaksi:")
        st.dataframe(df)
        st.download_button(
            label="Download Data Transaksi",
            data=convert_df_to_excel(df),
            file_name='transaksi.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.warning("Database belum tersedia. Lakukan transaksi terlebih dahulu untuk membuat database.")

# Fungsi untuk mengonversi DataFrame ke Excel untuk diunduh
def convert_df_to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Transaksi")
    processed_data = output.getvalue()
    return processed_data
