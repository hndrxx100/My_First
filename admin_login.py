import psycopg2
from psycopg2 import sql, errors
from dotenv import load_dotenv
import os

load_dotenv()


class AdminLogin:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    @staticmethod
    def connection_to_db():
        try:
            conn = psycopg2.connect(
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                host=os.getenv('DB_HOST'),
                dbname=os.getenv('DB_NAME'),
                port=os.getenv('DB_PORT')
            )
            return conn
        except psycopg2.Error as err:
            print(f"Database connection error: {err}")
            return None

    def authentication(self, username=None, password=None):
        self.username = username
        self.password = password
        conn = self.connection_to_db()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()
                cursor.execute(
                    """
                    SELECT * FROM adminlogin WHERE Username = %s AND Password = %s
                    """, (self.username, self.password)
                )
                login_user = cursor.fetchone()
                return login_user

            except psycopg2.Error as err:
                print(f"Error signing in: {err}")
                return False

            finally:
                if cursor:
                    cursor.close()
                conn.close()

    @staticmethod
    def fetch_data(registration_type):
        conn = AdminLogin.connection_to_db()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()
                if registration_type == 'All':
                    cursor.execute(
                        'SELECT firstname, lastname, email, phonenumber, registration_type, '
                        'snackpreferences, extraservices FROM participants'
                    )
                    columns = [column[0] for column in cursor.description]
                    registrations = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    return registrations
                else:
                    cursor.execute(
                        'SELECT firstname, lastname, email, phonenumber, registration_type, '
                        'snackpreferences, extraservices FROM participants WHERE registration_type = %s',
                        (registration_type,)
                    )
                    columns = [column[0] for column in cursor.description]
                    registrations = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    return registrations

            except psycopg2.Error as err:
                print(f"Error fetching data: {err}")
                return []

            finally:
                if cursor:
                    cursor.close()
                conn.close()
        return []
