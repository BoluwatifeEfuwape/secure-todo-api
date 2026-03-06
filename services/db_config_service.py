from config import get_db_connection

class BaseService:

    def get_connection(self):
        return get_db_connection()

    def close_connection(self, conn, cursor):
        cursor.close()
        conn.close()