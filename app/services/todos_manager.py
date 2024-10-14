from app.db.connection import get_db_connection
from app.models.todos import TodoStatus
from psycopg2.extras import RealDictCursor


# methods for todo
class TodoManager:
    def get_by_user_id(self, user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM todos WHERE user_id = %s ORDER BY id"
        cur.execute(query, (user_id,))
        todos = cur.fetchall()
        cur.close()
        conn.close()
        return todos

    def get_all(self):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM todos ORDER BY id")
        todos = cur.fetchall()
        cur.close()
        conn.close()
        return todos

    def get_by_id(self, todo_id, user_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM todos WHERE id = %s AND user_id = %s"
        cur.execute(query, (todo_id, user_id))
        todo = cur.fetchone()
        cur.close()
        conn.close()
        return todo

    def create(
            self, title, description="",
            status=TodoStatus.PENDENTE.value,
            user_id=None):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = (
            "INSERT INTO todos (title, description, status, user_id) "
            "VALUES (%s, %s, %s, %s) RETURNING *"
        )
        cur.execute(query, (title, description, status, user_id))
        new_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return new_todo

    def update(
            self, todo_id, title=None,
            description=None, status=None, user_id=None):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        set_clause = []
        params = []

        if title is not None:
            set_clause.append("title = %s")
            params.append(title)
        if description is not None:
            set_clause.append("description = %s")
            params.append(description)
        if status is not None:
            set_clause.append("status = %s")
            params.append(status)

        params.append(todo_id)
        params.append(user_id)

        query = (
            "UPDATE todos SET "
            f"{', '.join(set_clause)} "
            "WHERE id = %s AND user_id = %s RETURNING *"
        )

        cur.execute(query, params)
        updated_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return updated_todo

    def update_status(self, todo_id, new_status):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        query = "UPDATE todos SET status = %s WHERE id = %s RETURNING *"
        cur.execute(query, (new_status, todo_id))

        updated_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

        return updated_todo

    def delete(self, todo_id, user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        query = "DELETE FROM todos WHERE id = %s AND user_id = %s"
        cur.execute(query, (todo_id, user_id))
        conn.commit()
        cur.close()
        conn.close()
        return True
