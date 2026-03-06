from flask import Blueprint, request, jsonify
from config import get_db_connection, token_required
from services.todo_service import TodoService

todos_bp = Blueprint('todos', __name__)
todo_service = TodoService()

#we are creating 6 endpoints


#1 Get all todos

@todos_bp.route('', methods= ['GET'])
@token_required

def get_todos(user_id):
    
    try:

        todos = todo_service.get_all_todos(user_id)

        return jsonify(todos), 200
   
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500


#2 POST create todo

@todos_bp.route('', methods=['POST'])
@token_required

def create_todo(user_id):
    try:

        data = request.get_json()
        new_todo = todo_service.create_new_todo(user_id,data)

        return jsonify(new_todo), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    

    except Exception as e:
            print(f"Error: {e}")
            return jsonify({'error': 'Database error'}), 500
    
#3 GET single todo

@todos_bp.route('/<int:id>', methods=['GET'])
@token_required

def get_single_todo(user_id, id):
    try:
        
        single_todo = todo_service.get_todo(user_id, id)

        if not single_todo:
            return jsonify({'error': 'Todo not found'}), 404
        return jsonify(single_todo), 200
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500

            
#4 PUT update todo

@todos_bp.route('/<int:id>', methods=['PUT'])
@token_required

def update_todo(user_id, id):
    try:
        data = request.get_json()
        
        updated_todo = todo_service.update_todo(user_id, id, data)
        return jsonify(updated_todo), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500

#5 PATCH toggle completed

@todos_bp.route('/<int:id>/toggle', methods=['PATCH'])
@token_required

def toggle_single_todo(user_id, id):
    try:
        toggled_todo = todo_service.toggle_todo(user_id,id)
        return jsonify(toggled_todo), 200
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
        
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500


#6 DELETE todo

@todos_bp.route('/<int:id>', methods=['DELETE'])
@token_required

def delete_single_todo(user_id,id):
    try:
        
        todo_service.delete_todo(user_id,id)
        return '', 204
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 404  
             
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Database error'}), 500
    
