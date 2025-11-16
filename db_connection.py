import pymysql 

DB_HOST = 'mysql.railway.internal'
DB_PORT = int('3306')
DB_USER = 'root'
DB_PASSWORD = 'bIkYSqHLCIThFNtXAGOHxulwtPFGzubi'
DB_NAME = 'railway'

def connect_to_db():  
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        db=DB_NAME,
        port=DB_PORT
    )
    return connection

def create_table():
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
