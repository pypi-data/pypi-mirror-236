import pymysql
import re
import os

def create_connection():
    connection = pymysql.connect(
        host=os.environ.get('MYSQL_HOST'),
        user=os.environ.get('MYSQL_USER'),
        password=os.environ.get('MYSQL_PASSWORD'),
        db=os.environ.get('MYSQL_DATABASE'),
    )
    return connection

def clean_abusive_words(connection, input_text):
    words = re.findall(r'\b\w+\b|[.,\/#?!$%\^&\*;:{}=\-_`~()&+]|[-\d]+', input_text)
    clean_text = ''

    with connection.cursor() as cursor:
        for word in words:
            if word.isalnum():  
                cursor.execute("SELECT versi_halus FROM kata_kasar WHERE kata = %s", (word,))
                result = cursor.fetchone()
                if result:
                    kata_halus = result[0]
                    if word.istitle():
                        kata_halus = kata_halus.capitalize()
                    clean_text += ' ' + kata_halus
                else:
                    clean_text += ' ' + word
            else:
                clean_text += word

    clean_text = clean_text.strip()
    clean_text = re.sub(r'\s+', ' ', clean_text)
    clean_text = re.sub(r'\s*-\s*', ' - ', clean_text)

    return clean_text

def abusiveword_filter(input_text):
    connection = create_connection()
    try:
        cleaned_text = clean_abusive_words(connection, input_text)
        return cleaned_text
    finally:
        connection.close()