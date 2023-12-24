# api/v1/routes/orders.py
import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.models.order.order_status import OrderStatus

router = APIRouter()

# 示例订单数据库，实际中应该是从数据库中获取
fake_orders_db = {
    1: {"status": OrderStatus.PENDING_PAYMENT.value},
    2: {"status": OrderStatus.PROCESSING.value},
}

# 示例用户数据库，实际中应该是从数据库中获取
fake_users_db = {
    "fakeuser": {
        "username": "fakeuser",
        "password": "fakepassword",
        "disabled": False,
    }
}

# JWT相关配置
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 共享的身份验证函数
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    if username not in fake_users_db:
        raise credentials_exception
    return fake_users_db[username]


@router.put("/orders/{order_id}/update_status")
async def update_order_status(order_id: int, order_update: OrderStatus, current_user: dict = Depends(get_current_user)):
    # 在这里执行更新订单状态的逻辑
    # ...
    # 检查用户权限
    if current_user.get("diaabled"):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 检查订单是否存在
    if order_id not in fake_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    # 检查新状态是否有效
    if not OrderStatus.is_valid_status(order_update.new_status.value):
        raise HTTPException(status_code=400, detail="Invalid status")

    # 更新订单状态
    fake_orders_db[order_id].status = order_update.new_status.value
    fake_orders_db[order_id].updated_at = datetime.utcnow()

    return {"message": "Order status updated successfully"}


@router.get("/orders/{order_id}/get_status")
async def get_order_status(order_id: int, current_user: dict = Depends(get_current_user)):
    # 在这里执行获取订单状态的逻辑
    # ...
    # 检查用户权限检查用户权限
    if current_user.get("diaabled"):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    # 检查订单是否存在
    if order_id not in fake_orders_db:
        raise HTTPException(status_code=404, detail="Order not found")

    # 获取订单状态
    order_status = fake_orders_db[order_id].status
    return {"order_id": order_id, "status": order_status}


