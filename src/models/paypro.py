from dataclasses import dataclass
from typing import Dict, Any
from datetime import date, datetime
from decimal import Decimal
from src.models.base import ReportData


@dataclass
class PayproReport(ReportData):
    order_id: int
    order_status_id: int
    order_status_name: str
    payment_method_id: int
    payment_method_name: str
    created_at: datetime
    billing_currency_code: str
    balance_currency_code: str
    country: str
    billing_price: Decimal
    product_id: int
    order_item_name: str
    billing_price_tax_refund: Decimal
    billing_price_refund: Decimal
    balance_vendor_amount: Decimal
    balance_pay_pro_amount: Decimal

    def to_dict(self) -> Dict[str, Any]:
        return {
            "day": self.day,
            "order_id": self.order_id,
            "order_status_id": self.order_status_id,
            "order_status_name": self.order_status_name,
            "payment_method_id": self.payment_method_id,
            "payment_method_name": self.payment_method_name,
            "created_at": self.created_at,
            "billing_currency_code": self.billing_currency_code,
            "balance_currency_code": self.balance_currency_code,
            "country": self.country,
            "billing_price": self.billing_price,
            "product_id": self.product_id,
            "order_item_name": self.order_item_name,
            "billing_price_tax_refund": self.billing_price_tax_refund,
            "billing_price_refund": self.billing_price_refund,
            "balance_vendor_amount": self.balance_vendor_amount,
            "balance_pay_pro_amount": self.balance_pay_pro_amount,
        }
