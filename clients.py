import mysql.connector
from mysql.connector import errorcode


class Registrant:
    def __init__(self, firstname, lastname, email, phone, registration_type, snacks, extra_services):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.registration_type = registration_type
        self.snacks = snacks
        self.extra_services = extra_services

    def connection_to_db(self):
        try:
            conn = mysql.connector.connect(
                user='root',  # Replace with your MySQL username
                password='',  # Replace with your MySQL password
                host='localhost',  # Replace with your MySQL host
                database='registrations'  # Replace with your MySQL database name
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

    def create_user_table(self):
        conn = self.connection_to_db()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()

                # Corrected SQL for table creation
                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Participants (
                    ID INT AUTO_INCREMENT PRIMARY KEY,
                    FirstName VARCHAR(50) NOT NULL,
                    LastName VARCHAR(50) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    PhoneNumber VARCHAR(20) NOT NULL,
                    Registration_type VARCHAR(50) NOT NULL,
                    SnackPreferences VARCHAR(255),
                    ExtraServices TINYINT(1))
                    """
                )
                print("Users table created successfully")

            except mysql.connector.Error as err:
                print(f"Error creating table: {err}")

            finally:
                if cursor:
                    cursor.close()
                conn.close()

    def register(self, email, phone):
        conn = self.connection_to_db()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()

                # Check if the username or email already exists
                cursor.execute(
                    """
                    SELECT * FROM Participants WHERE Email = %s OR PhoneNumber = %s
                    """, (email, phone)
                )
                user = cursor.fetchone()
                return user

            except mysql.connector.Error as err:
                print(f"Error signing up: {err}")
                return None

            finally:
                if cursor:
                    cursor.close()
                conn.close()

    def insert(self, firstname, lastname, email, phone, registration_type, snacks, extra_services):
        conn = self.connection_to_db()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()

                # Insert the data into the table
                cursor.execute(
                    """
                    INSERT INTO Participants (Firstname, Lastname, Email, PhoneNumber, Registration_type, SnackPreferences, ExtraServices)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (firstname, lastname, email, phone, registration_type, snacks, extra_services)
                )
                conn.commit()
                print("User inserted successfully")

            except mysql.connector.Error as err:
                print(f"Error inserting user: {err}")

            finally:
                if cursor:
                    cursor.close()
                conn.close()
