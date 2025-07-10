# Web Scraping dan Text Preprocessing pada Data Class Central

Repositori ini berisi proyek scraping dan preprocessing teks dari situs [Class Central](https://www.classcentral.com/subject/cs), dengan fokus pada kursus-kursus bertema *Computer Science*. Proyek ini merupakan bagian dari tugas SISTECH 2025 untuk mengumpulkan data secara otomatis dari web dan melakukan pembersihan data teks sebelum analisis lanjutan.

## Tujuan

- Mengambil data kursus dari Class Central secara otomatis menggunakan Selenium.
- Melakukan pembersihan teks (text preprocessing) pada judul kursus agar siap digunakan untuk analisis teks seperti clustering, classification, atau keyword extraction.
- Menyimpan data bersih dalam format terstruktur (.csv dan .json).

## Tahapan Proyek

### 1. Web Scraping
Scraping dilakukan pada 10 halaman pertama kategori Computer Science di situs Class Central. Data yang diambil meliputi:

- `title`: Judul kursus
- `provider`: Platform penyedia kursus
- `language`: Bahasa pengantar kursus
- `certificate`: Ketersediaan sertifikat
- `avg_rating`: Rating rata-rata
- `is_free`: Status harga (gratis atau berbayar)
- `reviews`: Jumlah ulasan pengguna
- `link`: Link menuju halaman kursus

### 2. Text Preprocessing
Pembersihan teks dilakukan terhadap judul kursus dengan tahapan sebagai berikut:

- **Lowercasing**: Mengubah seluruh huruf menjadi huruf kecil.
- **Penghapusan noise**: Menghapus URL, tanda baca, angka, emoji, dan hashtag menggunakan Regular Expressions.
- **Stopwords removal**: Menghapus kata-kata umum yang tidak bermakna penting menggunakan daftar stopwords dari NLTK (Bahasa Inggris).
- **Stemming**: Mengubah kata ke bentuk dasar menggunakan `PorterStemmer` dari NLTK.

### 3. Penyimpanan Data
Setelah proses pembersihan, data disimpan dalam dua format:

- `classcentral.csv` – Format tabular yang mudah dibuka dengan Excel atau Pandas.
- `classcentral.json` – Format key-value untuk interoperabilitas dengan sistem lain.


## Struktur Output

| Kolom           | Deskripsi                                      |
|-----------------|-------------------------------------------------|
| Title           | Judul kursus asli                               |
| Provider        | Platform penyedia kursus                        |
| Language        | Bahasa pengantar kursus                         |
| Certificate     | Ketersediaan sertifikat (Yes/No)                |
| Average Rating  | Rating rata-rata (format: 4.75 ★)               |
| Price Type      | Gratis atau berbayar                            |
| Reviews         | Jumlah ulasan pengguna                          |
| Cleaned Title   | Judul kursus yang telah dibersihkan             |

## Link Google Colab

Notebook lengkap dapat dijalankan secara langsung melalui Google Colab:
https://colab.research.google.com/drive/1okFSPpk2ykvglDyRTAqEc8SXC5dmwe_Y?usp=sharing

## Dependencies

Library utama yang digunakan dalam proyek ini:

- `selenium`
- `webdriver-manager`
- `pandas`
- `nltk`
- `re`
- `json`
- `logging`

## Kontributor

**Keisha Hernantya Zahra**   
Mentee Hands On 1 Task - SISTECH 2025

