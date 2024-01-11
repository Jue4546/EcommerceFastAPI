from typing import Optional

from fastapi import APIRouter, HTTPException

from app.models.goods_model import BasicGoodsInfo, UpdateGoods, CreateGoods
from app.services.goods_service import (
    create_new_goods,
    remove_goods,
    get_goods_partial_id,
    admin_update_goods,
)

router = APIRouter()


# ok的
@router.post("/goods/create-goods", response_model=BasicGoodsInfo, tags=["商品管理模块"])
def create_goods(
        id: int,
        name: str,
        amount: int,
        unit_price: float,
        variety: str,
        color: str,
        occasion: str,
        description: str,
        image: str
):
    try:
        new_goods = CreateGoods(
            id=id,
            name=name,
            amount=amount,
            unit_price=unit_price,
            variety=variety,
            color=color,
            occasion=occasion,
            description=description,
            image=image,
        )
        return create_new_goods(new_goods, id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


# ok的
@router.delete("/goods/remove-goods/{goods_id}", response_model=BasicGoodsInfo, tags=["商品管理模块"])
def delete_goods(goods_id: int):
    try:
        return remove_goods(goods_id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


# ok的
@router.get("/goods/get-goods/{goods_id}/partial", response_model=list[BasicGoodsInfo], tags=["商品管理模块"])
def get_goods_partial(goods_id: int):
    try:
        return get_goods_partial_id(goods_id)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))


@router.put("/goods/update-goods/{goods_id}", response_model=UpdateGoods, tags=["商品管理模块"])  ##
def update_goods(
        goods_id: int,
        name: Optional[str] = None,
        amount: Optional[int] = None,
        unit_price: Optional[float] = None,
        variety: Optional[str] = None,
        color: Optional[str] = None,
        occasion: Optional[str] = None,
        description: Optional[str] = None,
        image: Optional[str] = None
):
    try:
        # 创建 UpdateGoods 类实例
        update_data = UpdateGoods(
            name=name,
            amount=amount,
            unit_price=unit_price,
            variety=variety,
            color=color,
            occasion=occasion,
            description=description,
            image=image,
        )

        # 创建一个字典，包含非空（非None）字段
        non_none_fields = {field: value for field, value in update_data.dict().items() if value is not None}

        # 检查非空字段
        if not non_none_fields:
            raise ValueError("至少提供一个非空字段进行更新。")

        # 调用 admin_update_goods 函数
        updated_goods = admin_update_goods(goods_id, non_none_fields)

        # 返回更新后的商品信息
        return updated_goods
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
