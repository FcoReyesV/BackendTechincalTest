from mysql.connector import pooling
from admin.domain.admin_model import Admin
from admin.application.superadmin_repository import ISuperAdminRepository


class MysqlAdminRepository(ISuperAdminRepository):
    def __init__(self, connection_pool: pooling.MySQLConnectionPool):
        self.__connection_pool = connection_pool

    def create(self, new_admin: Admin) -> bool:
        try:
            conn = self.__connection_pool.get_connection()
            cursor = conn.cursor()
            query = "INSERT INTO admins (username, password, email, is_superadmin) VALUES (%s, %s, %s, %s)"
            values = (new_admin.username, new_admin.password, new_admin.email, new_admin.is_superadmin)
            cursor.execute(query, values)
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()

    def get_by_id(self, field: str, key) -> Admin:
        try:
            conn = self.__connection_pool.get_connection()
            cursor = conn.cursor()
            query = f"SELECT * FROM admins WHERE {field} = %s"
            values = (key,)
            cursor.execute(query, values)
            result = cursor.fetchone()
            if not result:
                return None
            return Admin.admin_schema(result)
        finally:
            cursor.close()
            conn.close()

    def get_all(self) -> list[Admin]:
        try:
            conn = self.__connection_pool.get_connection()
            cursor = conn.cursor()
            query = "SELECT * FROM admins"
            cursor.execute(query)
            results = cursor.fetchall()
            return [Admin(**admin) for admin in results]
        except Exception:
            return []
        finally:
            cursor.close()
            conn.close()

    def update(self, admin_to_update: Admin) -> bool:
        try:
            conn = self.__connection_pool.get_connection()
            cursor = conn.cursor()
            query = "UPDATE admins SET username = %s, password = %s, email = %s, is_superadmin = %s WHERE admin_id = %s"
            values = (admin_to_update.username, admin_to_update.password, admin_to_update.email,
                      admin_to_update.is_superadmin, admin_to_update.admin_id)
            cursor.execute(query, values)
            if cursor.rowcount == 0:
                return False
            conn.commit()
            return True
        except Exception:
            return False
        finally:
            cursor.close()
            conn.close()

    def delete(self, field: str, key: str) -> bool:
        try:
            conn = self.__connection_pool.get_connection()
            cursor = conn.cursor()
            query = f"DELETE FROM admins WHERE {field} = %s"
            values = (key,)
            cursor.execute(query, values)
            if cursor.rowcount == 0:
                return False
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False
        finally:
            cursor.close()
            conn.close()
