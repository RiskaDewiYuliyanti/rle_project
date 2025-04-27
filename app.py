# app.py

import streamlit as st
from rle_model import rle_compress, rle_decompress, read_docx, save_to_docx
import tempfile
import os

st.set_page_config(page_title="Kompresi & Dekompresi RLE", layout="centered")

st.title("🗜️ Kompresi & Dekompresi Dokumen Word (.docx) - Algoritma RLE")

# Upload file
uploaded_file = st.file_uploader("Upload file Word (.docx)", type=["docx"])

# Pilih mode
mode = st.selectbox("Pilih Mode", ("Kompresi", "Dekompresi"))

# Tombol Eksekusi
if st.button("Proses"):
    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name

        # Baca isi file
        original_text = read_docx(tmp_path)

        # Proses Kompresi / Dekompresi
        if mode == "Kompresi":
            result_text = rle_compress(original_text)
            output_filename = "hasil_kompresi.docx"
        else:
            result_text = rle_decompress(original_text)
            output_filename = "hasil_dekompresi.docx"

        # Simpan hasil
        save_to_docx(result_text, output_filename)

        # Baca ulang file untuk download
        with open(output_filename, "rb") as f:
            file_bytes = f.read()

        st.success(f"Berhasil {mode.lower()} file!")
        st.download_button(
            label="⬇️ Download Hasil",
            data=file_bytes,
            file_name=output_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        # Hapus file sementara
        os.remove(tmp_path)
        os.remove(output_filename)
    else:
        st.error("Tolong upload file dulu ya!")
