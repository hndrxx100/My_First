import mysql.connector
from mysql.connector import errorcode


class AdminLogin:
    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    @staticmethod
    def connection_to_db():
        try:
            conn = mysql.connector.connect(
                user='hndrxx',
                password='Hndrxx_1000',
                host='localhost',
                database='registrations'
            )
            return conn
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
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

            except mysql.connector.Error as err:
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
                    cursor.execute('SELECT FirstName, LastName, Email, PhoneNumber, Registration_type, '
                                   'SnackPreferences, ExtraServices FROM participants')
                    columns = [column[0] for column in cursor.description]
                    registrations = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    return registrations
                else:
                    cursor.execute('SELECT FirstName, LastName, Email, PhoneNumber, Registration_type, '
                                   'SnackPreferences, ExtraServices FROM participants WHERE Registration_type = %s',
                                   (registration_type,))
                    columns = [column[0] for column in cursor.description]
                    registrations = [dict(zip(columns, row)) for row in cursor.fetchall()]
                    return registrations

            except mysql.connector.Error as err:
                print(f"Error fetching data: {err}")
                return []

            finally:
                if cursor:
                    cursor.close()
                conn.close()
        return []
