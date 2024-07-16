import psycopg2
from psycopg2 import sql, errors
from dotenv import load_dotenv
import os

load_dotenv()


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

    def create_user_table(self):
        conn = self.connection_to_db()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    CREATE TABLE IF NOT EXISTS Participants (
                    ID SERIAL PRIMARY KEY,
                    FirstName VARCHAR(50) NOT NULL,
                    LastName VARCHAR(50) NOT NULL,
                    Email VARCHAR(255) NOT NULL,
                    PhoneNumber VARCHAR(20) NOT NULL,
                    Registration_type VARCHAR(50) NOT NULL,
                    SnackPreferences VARCHAR(255),
                    ExtraServices BOOLEAN)
                    """
                )
                conn.commit()
                print("Participants table created successfully")

            except psycopg2.Error as err:
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

                cursor.execute(
                    """
                    SELECT * FROM Participants WHERE Email = %s OR PhoneNumber = %s
                    """, (email, phone)
                )
                user = cursor.fetchone()
                return user

            except psycopg2.Error as err:
                print(f"Error signing up: {err}")
                return None

            finally:
                if cursor:
                    cursor.close()
                conn.close()

    def insert(self, firstname, lastname, email, phone, registration_type, snacks, extra_services):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.registration_type = registration_type
        self.snacks = snacks
        self.extra_services = extra_services
        conn = self.connection_to_db()
        if conn:
            cursor = None
            try:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO Participants (FirstName, LastName, Email, PhoneNumber, Registration_type, SnackPreferences, ExtraServices)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """, (self.firstname, self.lastname, self.email, self.phone, self.registration_type, self.snacks,
                          self.extra_services)
                )
                conn.commit()
                print("Participant inserted successfully")

            except psycopg2.Error as err:
                print(f"Error inserting user: {err}")

            finally:
                if cursor:
                    cursor.close()
                conn.close()
