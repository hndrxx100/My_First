import mysql.connector
from mysql.connector import errorcode
from admin_login import AdminLogin


def create_table():
    conn = AdminLogin.connection_to_db()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS Enquiries(
                ID INT AUTO_INCREMENT PRIMARY KEY,
                FullName VARCHAR(50) NOT NULL,
                Email VARCHAR(50) NOT NULL,
                Message VARCHAR(255) NOT NULL
                )
                """
            )
            conn.commit()

        except mysql.connector.Error as err:
            print(f"Connection Error: {err}")
            return []

        finally:
            if cursor:
                cursor.close()
            conn.close()
    return []


def insert_enquiry_data(full_name, email, message):
    create_table()
    conn = AdminLogin.connection_to_db()
    if conn:
        cursor = None
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO Enquiries (FullName, Email, Message) VALUES (%s, %s, %s)
                """, (full_name, email, message)
            )
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error Inserting Data: {err}")
            return []

        finally:
            if cursor:
                cursor.close()
            conn.close()
    return []
