from decouple import config
import pymysql

def create_connection():
    connection = pymysql.connect(
        host=config('DB_HOST'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        db=config('DB_NAME'),
    )
    return connection

def find_abusive_words(connection, text):
    text = text.lower()
    words = text.split()
    abusive_words = []

    with connection.cursor() as cursor:
        for word in words:
            cursor.execute("SELECT id, kata FROM kata_kasar WHERE %s LIKE CONCAT('%%', kata, '%%')", (word,))
            results = cursor.fetchall()
            if results:
                for result in results:
                    abusive_words.append(f"[{result[1]}](https://stopucapkasar.com/detail.php?id={result[0]})")

    return abusive_words

def abusiveword_detector(input_text):
    connection = create_connection()

    try:
        abusive_words = find_abusive_words(connection, input_text)
        if abusive_words:
            result = ', '.join(abusive_words)
        else:
            result = "Nothing found!"
    finally:
        connection.close()

    return result