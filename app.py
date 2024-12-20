import streamlit as st
from kasir import kasir_app
from database import database_app

page = st.sidebar.radio("Pilih Halaman", ("Kasir", "Database"))

if page == "Kasir":
    kasir_app()
elif page == "Database":
    database_app()
