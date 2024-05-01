import sqlite3
import uuid

class DatabaseHandler:
    """
        Set of database functions to handle all its life cicle with sqlite3
    """
    def __init__(self):
        self._db_prod_path = './data/db/database_prod.db'

    def generate_uuid(self):
        """ Generates new UUID so can be used as ID en some table """
        return str(uuid.uuid4())

    def create_tables(self):
        """ 
            This command creates a production DB if this not exist
        """
        try:
            with sqlite3.connect(self._db_prod_path) as db_conn:
                cursor = db_conn.cursor()

                # Create the table for Users
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Users (
                        u_id INTEGER PRIMARY KEY NOT NULL,
                        u_joined DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Create the table for audio messages
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Audios (
                        a_id CHAR(36) PRIMARY KEY NOT NULL,
                        a_name VARCHAR,
                        a_path VARCHAR,
                        a_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        u_id INTEGER,
                        FOREIGN KEY (u_id) REFERENCES Users (u_id) ON DELETE SET NULL
                    )
                """)
                db_conn.commit()

        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    # =========================================================================================== CREATE
    def postNewUser(self, user_id:int):
        """Create new user with the given user_id in the DB if this does not exist"""
        try:
            with sqlite3.connect(self._db_prod_path) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute("INSERT OR IGNORE INTO Users (u_id) VALUES (?)", (user_id,))
                db_conn.commit()

        except sqlite3.Error as e:
            print(f"Error inserting user: {e}")

    def postUserAudio(self, user_id:int) -> str:
        """
            Posts a new audio message for a specified user into the database.

            This function generates a unique audio message ID (`a_id`) and determines the
            next sequential audio message name (`a_name`) based on the current audio count
            associated with the given user ID (`user_id`). The audio message is inserted
            into the 'Audios' table in the database.

            Args:
                user_id (int): The user ID associated with the audio message.

            Returns:
                str: The name of the newly created audio message (`a_name`).
            
            Note:
                Because this function uses an SQLite database to store and manage audio data
                locally (not in the cloud), it determines the next sequential ID for audio
                messages within the database. This approach ensures each audio message is
                uniquely identified and ordered chronologically within the database, also ensures 
                scalability because in scenarios with a large number of audio files, directly 
                counting files in the folder (the other approach) could be inefficient and time-consuming.
        """
        # Create the user if this does not exist
        self.postNewUser(user_id=user_id)
        # Obtain the user Audio count
        next_audio_id = self.getUserAudioCount(user_id=user_id)
        # Create the new audio message name
        a_msg_name = f'audio_message_{next_audio_id}'
        # Obtain new Audio Path
        a_path = f'/data/{user_id}/audio_data/{a_msg_name}.wav'
        # Obtain new Audio UID
        a_id = self.generate_uuid()

        # Add new Audio record into DB: (a_id, a_name, a_path, a_timestamp, u_id -> User)
        try:
            with sqlite3.connect(self._db_prod_path) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute("""
                    INSERT OR IGNORE INTO Audios (a_id, a_name, a_path, u_id)
                    VALUES (?,?,?,?)
                """, (a_id, a_msg_name, a_path, user_id))
                db_conn.commit()
        
        except sqlite3.Error as e:
            print(f"Error inserting audi: {e}")

        return a_msg_name
    
    # GET: Just for check purposes ================================================================ 
    def getUserAudioCount(self, user_id:int) -> int:
        """ Makes a GET request to the DB that returns the user's Audio messages number, 
            useful to obtain the next audio N for the audio name "audio_message_N"
        
        Args:
            user_id (int): The user ID in Telegram, which is also used in our file management
        Returns: (int)
        """
        try:
            with sqlite3.connect(self._db_prod_path) as db_conn:
                cursor = db_conn.cursor()
                cursor.execute("""SELECT COUNT(*) FROM Audios WHERE u_id = ?""", (user_id,))
                user_audios_count = cursor.fetchone()[0]
                db_conn.commit()
                
                return user_audios_count
        except sqlite3.Error as e:
            print(f"Error couting audios: {e}")