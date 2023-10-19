import pymysql
import re

# Fungsi untuk membuat koneksi ke database MySQL
def create_connection():
    connection = pymysql.connect(
        host='srv1092.hstgr.io',
        user='u378661453_root',
        password='Katakasar123!',
        db='u378661453_katakasar',
    )
    return connection

# Fungsi untuk membersihkan kalimat dari kata kasar
def clean_abusive_words(connection, input_text):
    words = re.findall(r'\b\w+\b|[.,\/#?!$%\^&\*;:{}=\-_`~()&+]|[-\d]+', input_text)
    clean_text = ''

    with connection.cursor() as cursor:
        for word in words:
            if word.isalnum():  # Cek apakah kata mengandung huruf atau angka
                # Query untuk mencari kata kasar dalam database
                cursor.execute("SELECT versi_halus FROM kata_kasar WHERE kata = %s", (word,))
                result = cursor.fetchone()

                if result:
                    # Jika kata kasar ditemukan dalam database, ganti dengan versi halus
                    kata_halus = result[0]
                    # Sesuaikan huruf besar atau kecilnya
                    if word.istitle():
                        kata_halus = kata_halus.capitalize()
                    # Tambahkan kata ke kalimat bersih
                    clean_text += ' ' + kata_halus
                else:
                    # Jika kata tidak ditemukan dalam database, gunakan kata asli
                    # Tambahkan kata ke kalimat bersih
                    clean_text += ' ' + word
            else:
                # Jika itu adalah tanda baca atau angka, tambahkan tanda baca tersebut ke kalimat tanpa perubahan
                clean_text += word

    # Hilangkan spasi ekstra di awal dan akhir kalimat
    clean_text = clean_text.strip()

    # Ganti semua spasi ganda dengan satu spasi
    clean_text = re.sub(r'\s+', ' ', clean_text)

    # Ganti semua tanda hubung dengan spasi di antara kata-kata
    clean_text = re.sub(r'\s*-\s*', ' - ', clean_text)

    return clean_text

# Contoh penggunaan
def abusiveword_filter(input_text):
    connection = create_connection()

    try:
        # Membersihkan kata kasar dari teks
        cleaned_text = clean_abusive_words(connection, input_text)
        return cleaned_text
    finally:
        connection.close()