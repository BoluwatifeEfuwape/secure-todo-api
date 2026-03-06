from .db_config_service import BaseService
from flask import Blueprint, request, jsonify

class TodoService(BaseService):
    #1 Get all todos
    def get_all_todos(self, user_id):
    # Connect to database
    # Query: SELECT * FROM todos
    # Return JSON list

        # Get query parameters for filtering
        completed = request.args.get('completed')  # ?completed=true
        priority = request.args.get('priority')    # ?priority=high
        
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Build query dynamically
        query = 'SELECT * FROM todos WHERE user_id = %s'
        params = [user_id]
        
        query += ' ORDER BY created_at DESC'
        
        cursor.execute(query, params)
        todos = cursor.fetchall()
        
        self.close_connection(conn, cursor)
        
        return todos
    
    #2 create todo    
    def create_new_todo(self,user_id,data):
        
            
        title = data.get('title')
        description = data.get('description', '')
        priority = data.get('priority', 'medium')
        due_date = data.get('due_date')
            
        # Validate
        if not user_id:
            return jsonify({'error': 'user_id is required'}), 400
            
        if not title:
            return jsonify({'error': 'Title is required'}), 400
            
        if priority not in ['low', 'medium', 'high']:
            return jsonify({'error': 'Priority must be low, medium, or high'}), 400
            
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
            
        # Insert todo
        cursor.execute(
            '''INSERT INTO todos (user_id, title, description, priority, due_date) 
            VALUES (%s, %s, %s, %s, %s)''',
            (user_id, title, description, priority, due_date)
            )
        conn.commit()
            
        # Get created todo
        todo_id = cursor.lastrowid
        cursor.execute('SELECT * FROM todos WHERE id = %s', (todo_id,))
        new_todo = cursor.fetchone()
            
        self.close_connection(conn, cursor)

        return new_todo
            
    #3 single_todo

    def get_todo(self, user_id, id):

        
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute(
            'SELECT * FROM todos WHERE id = %s AND user_id = %s',
            (id, user_id)
        )
        todo = cursor.fetchone()
    
        self.close_connection(conn, cursor)

        return todo
    
    #4 update information

    def update_todo(self, user_id, id, data):
    
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if todo exists
        cursor.execute(
            'SELECT * FROM todos WHERE id = %s AND user_id = %s',
            (id, user_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            self.close_connection(conn, cursor)
            raise ValueError("Todo not found")
        
        # Update todo
        cursor.execute(
            '''UPDATE todos 
               SET title = %s, description = %s, completed = %s, 
                   priority = %s, due_date = %s 
               WHERE id = %s''',
            (data.get('title', existing['title']),
             data.get('description', existing['description']),
             data.get('completed', existing['completed']),
             data.get('priority', existing['priority']),
             data.get('due_date', existing['due_date']),
             id)
        )
        conn.commit()
        
        # Get updated todo
        cursor.execute('SELECT * FROM todos WHERE id = %s', (id,))
        updated_todo = cursor.fetchone()
        
        self.close_connection(conn, cursor)
        
        return updated_todo
    

    # 5 toggle 
    def toggle_todo(self,user_id, id):
        
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if exists
        cursor.execute(
            'SELECT * FROM todos WHERE id = %s AND user_id = %s',
            (id, user_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            self.close_connection(conn, cursor)
            raise ValueError ("Todo not found")
        
        # Toggle completed
        new_status = 0 if existing['completed'] else 1
        cursor.execute(
            'UPDATE todos SET completed = %s WHERE id = %s',
            (new_status, id)
        )
        conn.commit()
        
        # Get updated todo
        cursor.execute('SELECT * FROM todos WHERE id = %s', (id,))
        updated_toggled_todo = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        return updated_toggled_todo  
                  
    #6 Delete      

    def delete_todo(self,user_id,id):
    
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Check if exists
        cursor.execute(
            'SELECT * FROM todos WHERE id = %s AND user_id = %s',
            (id, user_id)
        )
        existing = cursor.fetchone()
        
        if not existing:
            self.close_connection(conn, cursor)
            raise ValueError ("Todo not found")
        
        # Delete
        cursor.execute('DELETE FROM todos WHERE id = %s', (id,))
        conn.commit()
        
        self.close_connection(conn, cursor)
        
        return None
            