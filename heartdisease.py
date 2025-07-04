import streamlit as st
import pandas as pd
import pickle
import time
from PIL import Image

# Konfigurasi halaman
st.set_page_config(page_title="Heart Disease Prediction", layout="wide")
st.title("Heart Disease Prediction App")

# Header deskripsi
st.markdown("""
Aplikasi ini dibuat dengan harapan dapat membantu Anda dalam memprediksi **Penyakit Jantung**. Dibuat oleh [@angelinert](https://www.linkedin.com/in/angeline-riendra-tatipang-3a868528b/)

Data diperoleh dari [Heart Disease dataset](https://archive.ics.uci.edu/dataset/45/heart+disease) oleh UC Irvine.
""")

# Gambar
img = Image.open("pict2.jpg")
st.image(img, width=500)

# Deskripsi fitur
with st.expander("Deskripsi Fitur", expanded=False):
    st.markdown("""
1. **cp (Tipe Nyeri Dada)**  
   Digunakan untuk mengklasifikasikan jenis nyeri dada yang dirasakan pasien:
   - `1 = Typical angina` → Nyeri dada klasik karena penyempitan pembuluh darah jantung.  
   - `2 = Atypical angina` → Nyeri dada tidak khas, bisa berasal dari jantung tapi tidak jelas.  
   - `3 = Non-anginal pain` → Nyeri dada bukan berasal dari jantung, misalnya karena otot atau pencernaan.  
   - `4 = Asymptomatic` → Tidak merasakan nyeri dada sama sekali.

2. **thalach (Detak Jantung Maksimum)**  
   Jumlah detak jantung tertinggi yang dicapai pasien saat uji stres atau latihan. Angka tinggi menunjukkan jantung bekerja keras.

3. **slope (Kemiringan ST)**  
   Bentuk kemiringan segmen ST pada hasil EKG setelah latihan:
   - `0 = Upsloping` → Segmen ST naik, sering dianggap normal.  
   - `1 = Flat` → Segmen ST datar, bisa menunjukkan risiko penyakit jantung.  
   - `2 = Downsloping` → Segmen ST turun, sering dikaitkan dengan gangguan jantung yang serius.

4. **oldpeak (Depresi ST)**  
   Penurunan segmen ST setelah latihan. Semakin besar angkanya, semakin besar kemungkinan ada masalah aliran darah ke jantung.

5. **exang (Angina karena olahraga)**  
   Apakah pasien mengalami nyeri dada saat olahraga:
   - `0 = Tidak`  
   - `1 = Ya`

6. **ca (Jumlah pembuluh besar)**  
   Jumlah pembuluh darah utama yang terlihat melalui pencitraan (angiografi):
   - `0–3` → Semakin banyak pembuluh yang terlihat tersumbat, semakin tinggi risikonya.

7. **thal (Hasil Tes Thalassemia)**  
   Hasil tes pemindaian thalassemia untuk melihat kondisi aliran darah di jantung:
   - `1 = Normal`  
   - `2 = Fixed defect` → Aliran darah terhambat secara permanen.  
   - `3 = Reversible defect` → Hambatan aliran darah yang mungkin membaik dengan pengobatan.

8. **sex (Jenis Kelamin)**  
   - `0 = Perempuan`  
   - `1 = Laki-laki`

9. **age (Usia)**  
   Usia pasien dalam tahun. Usia tua meningkatkan risiko penyakit jantung.
""", unsafe_allow_html=True)


# Sidebar untuk input user
st.sidebar.title("📝 Input Data Pasien")
st.sidebar.write("Masukkan data Anda untuk masing-masing fitur di bawah ini:")

def user_input_features():
    cp = st.sidebar.slider('Tipe Nyeri Dada (1-4)', 1, 4, 2)
    thalach = st.sidebar.slider("Detak Jantung Maksimum (71–202)", 71, 202, 150)
    slope = st.sidebar.slider("Kemiringan ST (0=up, 1=flat, 2=down)", 0, 2, 1)
    oldpeak = st.sidebar.slider("Oldpeak (0.0–6.2)", 0.0, 6.2, 1.0)
    exang = st.sidebar.radio("Angina karena olahraga", ["Tidak", "Ya"])
    ca = st.sidebar.slider("Jumlah Pembuluh Besar (0–3)", 0, 3, 0)
    thal = st.sidebar.slider("Hasil Tes Thalassemia (1–3)", 1, 3, 2)
    sex = st.sidebar.radio("Jenis Kelamin", ["Perempuan", "Laki-laki"])
    age = st.sidebar.slider("Usia", 29, 77, 50)

    # Mapping kategori ke numerik
    exang_val = 1 if exang == "Ya" else 0
    sex_val = 1 if sex == "Laki-laki" else 0

    data = {
        'cp': cp,
        'thalach': thalach,
        'slope': slope,
        'oldpeak': oldpeak,
        'exang': exang_val,
        'ca': ca,
        'thal': thal,
        'sex': sex_val,
        'age': age
    }
    features = pd.DataFrame(data, index=[0])
    return features

# Ambil input user
input_df = user_input_features()

# Buat DataFrame baru dengan penjelasan
row = input_df.iloc[0]  # Ambil satu baris user input
interpretasi = {
    'cp': {
        1: "Typical angina",
        2: "Atypical angina",
        3: "Non-anginal pain",
        4: "Asymptomatic"
    },
    'slope': {
        0: "Upsloping",
        1: "Flat",
        2: "Downsloping"
    },
    'exang': {
        0: "Tidak",
        1: "Ya"
    },
    'thal': {
        1: "Normal",
        2: "Fixed defect",
        3: "Reversible defect"
    },
    'sex': {
        0: "Perempuan",
        1: "Laki-laki"
    }
}

# Buat list hasil interpretasi
deskripsi_input = {
    'cp': interpretasi['cp'].get(row['cp'], "-"),
    'thalach': "Detak jantung maksimum (bpm)",
    'slope': interpretasi['slope'].get(row['slope'], "-"),
    'oldpeak': "ST depression: {:.1f}".format(row['oldpeak']),
    'exang': interpretasi['exang'].get(row['exang'], "-"),
    'ca': f"{row['ca']} pembuluh besar terlihat",
    'thal': interpretasi['thal'].get(row['thal'], "-"),
    'sex': interpretasi['sex'].get(row['sex'], "-"),
    'age': f"{row['age']} tahun"
}

# Gabungkan ke dalam DataFrame
combined_df = pd.DataFrame({
    'Fitur': row.index,
    'Nilai': row.values,
    'Penjelasan': [deskripsi_input[k] for k in row.index]
})

# Tampilkan
st.subheader("📋 Data Pasien")
st.dataframe(combined_df, use_container_width=True)

# Ambil nilai dari DataFrame
row = input_df.iloc[0]

# Tombol prediksi
if st.button("Prediksi", use_container_width=True):
    df = input_df
    st.subheader("Hasil Prediksi")
    try:
        with open("best_classifier.pkl", 'rb') as file:
            loaded_model = pickle.load(file)

        # Gunakan .values agar aman jika model dilatih tanpa feature names
        prediction = loaded_model.predict(df)

        with st.spinner('Memprediksi...'):
            time.sleep(2)
            if prediction[0] == 0:
                result_html = """
                <div style="background-color:#14532d; color:white; padding:1rem; border-radius:10px;
                            font-size:18px; font-weight:bold;">
                    Tidak Terdeteksi Penyakit Jantung
                </div>
                """
            else:
               prediction[0] == 1
               result_html = """
                <div style="background-color:#7f1d1d; color:white; padding:1rem; border-radius:10px;
                            font-size:18px; font-weight:bold;">
                    Terdeteksi Penyakit Jantung
                </div>
                """

            st.markdown(result_html, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("❌ Model belum ditemukan. Pastikan file `heartdisease1.pkl` tersedia di direktori.")
    except Exception as e:
        st.error(f"❌ Terjadi error saat memuat model: {e}")

      