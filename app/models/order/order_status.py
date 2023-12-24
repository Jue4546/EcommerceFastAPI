#  models/order/order_status.py
from enum import Enum


class OrderStatus(Enum):
    """
    订单状态
    """
    PENDING_PAYMENT = "待支付"
    PROCESSING = "处理中"
    PAID = "已支付"
    PACKING = "已发货"
    IN_TRANSIT = "运输中"
    SHIPPED = "已收货"
    DELIVERED = "已交付"
    COMPLITED = "已完成"
    CANCELED = "已取消"
    RETURNED = "已退货"
    REFUNDED = "已退款"
    REFUND_FAILED = "退款失败"
    REFUND_SUCCESS = "退款成功"
    REFUND_PENDING = "退款中"
    REFUND_REJECTED = "退款被拒绝"
    REFUND_CANCELED = "退款取消"

    @classmethod
    def is_valid_status(cls, status):
        # 判断状态是否有效
        # 此方法返回一个布尔值，表示传入的状态是否存在于'OrderStatus'类的字典中
        return status in cls.__dict__.values()


'''
    使用方法的例子：
    from models.order.order_status import OrderStatus

    # 示例状态
    status_to_check = "已支付"

    # 检查状态是否有效
    if OrderStatus.is_valid_status(status_to_check):
        print(f"{status_to_check} 是有效的订单状态。")
    else:
        print(f"{status_to_check} 不是有效的订单状态。")

'''
