"""用户模型的 CRUD 操作：db/crud/user_crud.py"""
from typing import Union, List

from app.db.base import get_db_connection
from app.models.user_model import RegisterUser, UserInDB, BaseUser


def create_user(user: RegisterUser) -> BaseUser:
    """创建新用户并将其添加到数据库"""
    db = get_db_connection()
    cursor = db.cursor()
    insert_query = ("INSERT INTO users (username, email, full_name, disabled, admin, password) VALUES "
                    "(%s, %s, %s, %s, %s, %s)")
    cursor.execute(insert_query, (user.username, user.email, user.full_name, user.disabled, user.admin,
                                  user.hashed_password))
    db.commit()
    new_user_id = cursor.lastrowid
    cursor.close()
    db.close()
    return BaseUser(username=user.username, email=user.email, full_name=user.full_name,
                    disabled=user.disabled, admin=user.admin)


def get_user(username: str, mode: str = None) -> Union[UserInDB, BaseUser, None]:
    """根据用户名从数据库中获取用户信息"""
    db = get_db_connection()
    cursor = db.cursor()
    select_query = ("SELECT id, username, email, password, full_name, disabled, admin FROM users "
                    "WHERE username = %s")
    cursor.execute(select_query, (username,))
    user_data = cursor.fetchone()
    cursor.close()
    db.close()
    if user_data:
        if mode == 'normal':
            curr_user = BaseUser(
                username=user_data[1],
                email=user_data[2],
                full_name=user_data[4],
                disabled=user_data[5],
                admin=user_data[6]
            )
        else:
            curr_user = UserInDB(
                id=user_data[0],
                username=user_data[1],
                email=user_data[2],
                hashed_password=user_data[3],
                full_name=user_data[4],
                disabled=user_data[5],
                admin=user_data[6]
            )
        return curr_user
    else:
        return None


def get_all_users() -> List[BaseUser]:
    """从数据库中获取所有用户信息"""
    db = get_db_connection()
    cursor = db.cursor()
    select_all_query = "SELECT id, username, email, password, full_name, disabled, admin FROM users"
    cursor.execute(select_all_query)
    users_data = cursor.fetchall()
    cursor.close()
    db.close()
    users_db = [BaseUser(username=user_data[1],
                         email=user_data[2],
                         full_name=user_data[4],
                         disabled=user_data[5],
                         admin=user_data[6]
                         ) for user_data in users_data]
    return users_db


def check_existing_user_by_email(email: str) -> bool:
    """根据邮箱判断用户是否存在"""
    db = get_db_connection()
    cursor = db.cursor()
    select_query = "SELECT COUNT(*) FROM users WHERE email = %s"
    cursor.execute(select_query, (email,))
    count = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return count > 0


def check_existing_user_by_name(username: str) -> bool:
    """根据用户名判断用户是否存在"""
    db = get_db_connection()
    cursor = db.cursor()
    select_query = "SELECT COUNT(*) FROM users WHERE username = %s"
    cursor.execute(select_query, (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    db.close()
    return count > 0


def update_user(user_id: int, new_data: dict) -> bool:
    """根据用户ID更新用户信息"""
    db = get_db_connection()
    cursor = db.cursor()
    update_query = "UPDATE users SET username = %s, email = %s, password = %s WHERE id = %s"
    cursor.execute(update_query, (new_data['username'], new_data['email'], new_data['password'], user_id))
    db.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    db.close()
    return affected_rows > 0
