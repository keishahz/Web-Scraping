# Install semua library yang dibutuhkan
!pip install requests
!pip install selenium
!pip install -q google-colab-selenium
!pip install nltk
!pip install selenium webdriver-manager pandas

!apt-get update
!wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
!dpkg -i google-chrome-stable_current_amd64.deb || apt-get install -f -y

import requests
import selenium
import nltk
import random
import time
import pandas as pd
import logging
import string
import json
print("All libraries installed successfully!")

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

import copy
import google_colab_selenium as gs

# Menyiapkan konfigurasi logging untuk memantau proses scraping
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def setup():
  # Fungsi untuk menyiapkan dan mengembalikan WebDriver (Chrome) di Google Colab.
  # Menggunakan opsi headless dan beberapa flags tambahan agar dapat berjalan stabil.
  logging.info("Menyiapkan WebDriver untuk lingkungan Google Colab...")
  chrome_options = Options()
  chrome_options.add_argument("--headless")  # Menjalankan Chrome tanpa GUI
  chrome_options.add_argument("--no-sandbox")
  chrome_options.add_argument("--disable-dev-shm-usage")
  chrome_options.add_argument("--window-size=1920,1080")
  chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

  # Inisialisasi WebDriver menggunakan ChromeDriverManager
  driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
  logging.info("WebDriver berhasil disiapkan.")
  return driver

def scrape_classcentral(driver, base_url):
    # Melakukan scraping dari halaman-halaman Class Central berdasarkan URL dasar.
    all_courses_data = []
    logging.info(f"Memulai scraping dari: {base_url}")

    for page in range(1, 11):  # Halaman 1 sampai 10
        url = f"{base_url}?page={page}"
        logging.info(f"Scraping halaman {page}: {url}")
        driver.get(url)
        time.sleep(3)  # Jeda untuk memberi waktu halaman loading

        # Cari semua elemen yang merupakan nama kursus
        course_containers = driver.find_elements(By.CSS_SELECTOR, 'a.color-charcoal.course-name')
        logging.info(f"Halaman {page}: ditemukan {len(course_containers)} kursus.")

        for title_elem in course_containers:
            try:
                # Ambil teks judul dan link
                title = title_elem.text.strip()
                link = title_elem.get_attribute('href')

                # Ambil atribut JSON tersembunyi untuk informasi tambahan
                data_props_raw = title_elem.get_attribute('data-track-props')
                data_props = json.loads(data_props_raw)

                provider = data_props.get("course_provider", "Unknown")
                certificate = data_props.get("course_certificate", False)
                language = data_props.get("course_language", "N/A")
                avg_rating = data_props.get("course_avg_rating", 0.0)
                is_free = data_props.get("course_is_free", False)

                try:
                    # Coba ambil teks ulasan
                    reviews = title_elem.find_element(By.XPATH, '../..').find_element(By.CSS_SELECTOR, 'span.color-gray').text.strip()
                except:
                    reviews = "0 reviews"

                # Simpan data ke list
                all_courses_data.append({
                    'title': title,
                    'provider': provider,
                    'language': language,
                    'certificate': certificate,
                    'avg_rating': avg_rating,
                    'is_free': is_free,
                    'reviews': reviews,
                    'link': f"https://www.classcentral.com{link}"
                })

            except Exception as e:
                logging.warning(f"Error saat membaca 1 kursus di halaman {page}: {e}")
                continue

    # Konversi hasil scraping ke DataFrame
    return pd.DataFrame(all_courses_data)

# Inisialisasi WebDriver
driver = setup()

# URL target kategori kursus Computer Science
target_url = "https://www.classcentral.com/subject/cs"

# Jalankan scraping dan simpan ke DataFrame
scraped_data = scrape_classcentral(driver, target_url)

# Import Library Tambahan
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download resource NLTK untuk Bahasa Inggris
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab') 

print("Library berhasil di-import.")

# Menghapus URL, Hashtag, Emoji, Angka, dan Tanda Baca
def clean_noise(text):
  # Menghapus semua tag HTML secara utuh
  text = re.sub(r'<.*?>', '', text)
  # Menghapus URL
  text = re.sub(r'https?://\S+|www\.\S+', '', text)
  # Menghapus Hashtag
  text = re.sub(r'#\w+', '', text)
  # Menghapus Emoji dan Tanda Baca
  text = re.sub(r'[^\w\s]', '', text)
  # Menghapus Angka
  text = re.sub(r'\d+', '', text)
  # Menghapus spasi berlebih
  text = re.sub(r'\s+', ' ', text).strip()
  return text

# Menghapus Stopwords
# Define list_stopwords
from nltk.corpus import stopwords
list_stopwords = set(stopwords.words('english'))

def remove_stopwords(text):

  # Memecah kalimat menjadi kata-kata (tokenization)
  tokens = text.split()

  # Menghapus stopwords dari daftar token
  tokens_without_stopwords = [word for word in tokens if word not in list_stopwords]

  # Menggabungkan kembali token menjadi kalimat
  text = ' '.join(tokens_without_stopwords)
  return text

# Stemming
# Membuat stemmer
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

def cleaning_pipeline(text):
  text = text.lower()
  text = clean_noise(text)
  text = remove_stopwords(text)
  text = stemmer.stem(text)
  return text

# Menjalankan Pipeline Lengkap
driver = setup()
df = pd.DataFrame()

try:
    target_url = "https://www.classcentral.com/subject/cs"
    df = scrape_classcentral(driver, target_url)

    if not df.empty:
        logging.info("\nScraping berhasil. Memulai pipeline preprocessing...")

        # Terapkan Preprocessing ke Kolom Judul
        text_before = df['title'].iloc[0] # Simpan contoh teks asli
        df['cleaned_title'] = df['title'].apply(cleaning_pipeline)
        logging.info("Pipeline preprocessing selesai.")

        print("\n--- CONTOH HASIL PREPROCESSING (Data Pertama) ---")
        print(f"\n1. JUDUL ASLI:\n{text_before}")
        print(f"\n2. HASIL AKHIR:\n{df['cleaned_title'].iloc[0]}")

        # Format tambahan:
        df['is_free'] = df['is_free'].map({True: 'Free', False: 'Paid'})
        df['certificate'] = df['certificate'].map({True: 'Certificate Available', False: 'No Certificate'})
        df['avg_rating'] = df['avg_rating'].apply(lambda x: f"{x:.2f} ★" if x != "N/A" else x)

        # Susun kolom yang ingin disimpan
        final_df = df[['title', 'provider', 'language', 'certificate', 'avg_rating', 'is_free', 'reviews', 'cleaned_title']]
        final_df.columns = ['Title', 'Provider', 'Language', 'Certificate', 'Average Rating', 'Price Type', 'Reviews', 'Cleaned Title']

        # Simpan file CSV dan JSON
        output_file_csv = 'classcentral.csv'
        final_df.to_csv(output_file_csv, index=False)
        print(f"\nData bersih berhasil disimpan ke file: '{output_file_csv}'")

        output_file_json = 'classcentral.json'
        final_df.to_json(output_file_json, orient='records', indent=4)
        print(f"Data bersih berhasil disimpan ke file: '{output_file_json}'")

    else:
        logging.warning("Scraping tidak menghasilkan data. Tidak ada file yang disimpan.")

finally:
    driver.quit()
    logging.info("WebDriver ditutup.")
