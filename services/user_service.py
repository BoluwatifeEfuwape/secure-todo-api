from config import get_db_connection, hash_password, check_password, create_token

class UserService:
    def register_user(self, username, email, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Check duplicates
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise ValueError("Email already registered")

        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            raise ValueError("Username already taken")

        password_hash = hash_password(password)

        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)',
            (username, email, password_hash)
        )
        conn.commit()

        user_id = cursor.lastrowid
        cursor.execute('SELECT id, username, email, created_at FROM users WHERE id = %s', (user_id,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        token = create_token(user_id)
        return user, token

    def login_user(self, email, password):
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if not user or not check_password(user['password_hash'], password):
            raise ValueError("Invalid email or password")

        token = create_token(user['id'])
        return {
            'id': user['id'],
            'username': user['username'],
            'email': user['email']
        }, token