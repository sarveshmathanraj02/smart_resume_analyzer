# db_connection.py
import pymysql

DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'Sarvesh0209'
DB_NAME = 'sra'


def create_database():
    """Create the database if it does not exist."""
    conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD)
    cursor = conn.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.commit()
    conn.close()


def connect_to_db():
    """Connect to the database after ensuring it exists."""
    create_database()  # ← VERY IMPORTANT
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME
    )
    return connection


def create_table():
    """Create the user_data table if it does not exist."""
    connection = connect_to_db()
    cursor = connection.cursor()

    table_sql = """
        CREATE TABLE IF NOT EXISTS user_data(
            ID INT NOT NULL AUTO_INCREMENT,
            Name VARCHAR(100) NOT NULL,
            Email_ID VARCHAR(50) NOT NULL,
            resume_score VARCHAR(8) NOT NULL,
            Timestamp VARCHAR(50) NOT NULL,
            Page_no VARCHAR(5) NOT NULL,
            Predicted_Field VARCHAR(25) NOT NULL,
            User_level VARCHAR(30) NOT NULL,
            Actual_skills VARCHAR(300) NOT NULL,
            Recommended_skills VARCHAR(300) NOT NULL,
            Recommended_courses VARCHAR(600) NOT NULL,
            PRIMARY KEY (ID)
        );
    """
    cursor.execute(table_sql)
    connection.commit()
    connection.close()