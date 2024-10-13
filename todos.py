from enum import Enum
from db import get_db_connection
from psycopg2.extras import RealDictCursor


# todo status enums
class TodoStatus(Enum):
    PENDENTE = "pendente"
    INCOMPLETA = "incompleta"
    COMPLETA = "completa"


class TodoManager:
    def get_all(self):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM todos")
        todos = cur.fetchall()
        cur.close()
        conn.close()
        return todos

    def get_by_id(self, todo_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM todos WHERE id = %s", (todo_id,))
        todo = cur.fetchone()
        cur.close()
        conn.close()
        return todo

    def create(self, title, description="", status=TodoStatus.PENDENTE.value):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "INSERT INTO todos (title, description, status) "
            "VALUES (%s, %s, %s) RETURNING *",
            (title, description, status),
        )
        new_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return new_todo

    def update(self, todo_id, title=None, description=None, status=None):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            "UPDATE todos SET title = %s, description = %s, status = %s "
            "WHERE id = %s RETURNING *",
            (title, description, status, todo_id),
        )
        updated_todo = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        return updated_todo

    def delete(self, todo_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        conn.commit()
        cur.close()
        conn.close()
        return True
