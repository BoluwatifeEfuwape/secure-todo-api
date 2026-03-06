from flask import Blueprint, request, jsonify
from config import get_db_connection, hash_password, check_password, create_token
from services.user_service import UserService

users_bp = Blueprint('users', __name__)
user_service = UserService()

# Register new user
@users_bp.route('/register', methods=['POST'])

def register():
    try:
        data = request.get_json()
        user, token = user_service.register_user(

        data.get('username'),
        data.get('email'),
        data.get('password')
        
        )

        return jsonify({
            'message': 'User registered successfully',
            'token': token,
            'user': user
        }), 201

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500


# Login user
@users_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user, token = user_service.login_user(
        data.get('email'),
        data.get('password')
    )
    
        return jsonify({
            'message': 'Login successful',
            'token': token, 
            'user': user
            }), 200
    

    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500
