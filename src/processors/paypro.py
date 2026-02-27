import csv
import logging
from datetime import datetime
from decimal import Decimal
from typing import List
from src.models.base import ReportData
from src.models.paypro import PayproReport
from src.processors.base import ReportProcessor


class PayproReportProcessor(ReportProcessor):

    def process_data(self, file_path: str) -> List[ReportData]:
        reports = []
        failed_rows = []

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row_num, row in enumerate(reader, start=2):
                try:
                    created_at_str = row.get('createdAt', '1970-01-01T00:00:00.000')
                    created_at = datetime.strptime(created_at_str, '%Y-%m-%dT%H:%M:%S.%f')
                    day = created_at.date()

                    report = PayproReport(
                        day=day,
                        order_id=int(row.get('orderId', 0)),
                        order_status_id=int(row.get('orderStatusId', 0)),
                        order_status_name=row.get('orderStatusName', ''),
                        payment_method_id=int(row.get('paymentMethodId', 0)),
                        payment_method_name=row.get('paymentMethodName', ''),
                        created_at=created_at,
                        billing_currency_code=row.get('billingCurrencyCode', ''),
                        balance_currency_code=row.get('balanceCurrencyCode', ''),
                        country=row.get('country', ''),
                        billing_price=Decimal(row.get('billingPrice', '0')),
                        product_id=int(row.get('productId', 0)),
                        order_item_name=row.get('orderItemName', ''),
                        billing_price_tax_refund=Decimal(row.get('billingPriceTaxRefund', '0')),
                        billing_price_refund=Decimal(row.get('billingPriceRefund', '0')),
                        balance_vendor_amount=Decimal(row.get('balanceVendorAmount', '0')),
                        balance_pay_pro_amount=Decimal(row.get('balancePayProAmount', '0')),
                    )
                    reports.append(report)
                except (ValueError, KeyError) as e:
                    logging.error(f"Row {row_num} invalid: {row}. Error: {e}")
                    failed_rows.append((row_num, str(e)))

        if failed_rows:
            raise ValueError(f"Failed to parse {len(failed_rows)} rows: {failed_rows[:5]}")

        return reports

    def get_target_table(self) -> str:
        return "paypro_report"
