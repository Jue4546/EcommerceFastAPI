"""用户服务逻辑：services/user_service.py"""
from typing import List

from app.db.crud.user_crud import create_user, check_existing_user_by_email, check_existing_user_by_name, update_user, \
    get_all_users
from app.models.user_model import RegisterUser, BaseUser
from app.services.auth_service import get_password_hash


def is_valid_password(password: str) -> bool:
    """验证密码强度的函数，可以根据实际需求进行扩展"""
    # 例如：密码长度至少为8位，包含大小写字母、数字和特殊字符
    return len(password) >= 8 and any(c.isupper() for c in password) and any(c.islower() for c in password) and any(
        c.isdigit() for c in password) and any(not c.isalnum() for c in password)


def register_new_user(user: RegisterUser) -> BaseUser:
    """用户注册服务逻辑：验证用户信息并将其注册到数据库"""
    if check_existing_user_by_email(user.email):
        raise ValueError("该邮箱已被注册")
    if check_existing_user_by_name(user.username):
        raise ValueError("该用户名已被注册")
    if not is_valid_password(user.password):
        raise ValueError("密码不符合要求")

    # 对用户密码进行哈希加密
    user.hashed_password = get_password_hash(user.password)

    # 调用 CRUD 操作函数创建新用户
    return create_user(user)


def reset_password(user_email: str) -> bool:
    """重置用户密码的服务逻辑"""
    # todo
    return True


def update_user_info(user_id: int, new_data: BaseUser) -> bool:
    """更新用户信息的服务逻辑"""
    return update_user(user_id, new_data.__dict__)


def fetch_all_users() -> List[BaseUser]:
    """获取所有用户信息的服务逻辑"""
    return get_all_users()
