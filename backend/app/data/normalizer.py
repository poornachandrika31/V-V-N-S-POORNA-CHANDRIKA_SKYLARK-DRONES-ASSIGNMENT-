from datetime import datetime
from typing import Any


def clean_text(value: Any) -> str | None:
    if value is None:
        return None

    value = str(value).strip()

    if not value or value.lower() in {"nan", "none", "null"}:
        return None

    return value


def clean_number(value: Any) -> float | None:
    if value is None:
        return None

    try:
        text = str(value).replace(",", "").strip()

        if not text:
            return None

        return float(text)

    except (ValueError, TypeError):
        return None


def clean_date(value: Any) -> str | None:
    if not value:
        return None

    try:
        return str(value)[:10]
    except Exception:
        return None


def column_map(item: dict) -> dict:
    """
    Converts Monday column_values into:

        {
            "column_id": "displayed text value"
        }
    """

    result = {}

    for column in item.get("column_values", []):
        result[column["id"]] = clean_text(column.get("text"))

    return result


# ---------------------------------------------------------
# DEALS
# ---------------------------------------------------------

DEAL_COLUMNS = {
    "owner": "color_mm6qy680",
    "client_code": "dropdown_mm6qr4yd",
    "deal_status": "color_mm6qx4j9",
    "close_date": "date_mm6qwj6t",
    "probability": "color_mm6qv7g0",
    "deal_value": "numeric_mm6qeypw",
    "tentative_close_date": "date_mm6qxznv",
    "deal_stage": "color_mm6qk62d",
    "product": "color_mm6qz85s",
    "sector": "color_mm6qzqjs",
    "created_date": "date_mm6q39d0",
}


def normalize_deal(item: dict) -> dict:

    columns = column_map(item)

    return {
        "id": item.get("id"),
        "name": clean_text(item.get("name")),

        "owner": columns.get(DEAL_COLUMNS["owner"]),
        "client_code": columns.get(DEAL_COLUMNS["client_code"]),
        "deal_status": columns.get(DEAL_COLUMNS["deal_status"]),

        "close_date": columns.get(DEAL_COLUMNS["close_date"]),

        "probability": columns.get(
            DEAL_COLUMNS["probability"]
        ),

        "deal_value": clean_number(
            columns.get(DEAL_COLUMNS["deal_value"])
        ),

        "tentative_close_date": columns.get(
            DEAL_COLUMNS["tentative_close_date"]
        ),

        "deal_stage": columns.get(
            DEAL_COLUMNS["deal_stage"]
        ),

        "product": columns.get(
            DEAL_COLUMNS["product"]
        ),

        "sector": columns.get(
            DEAL_COLUMNS["sector"]
        ),

        "created_date": columns.get(
            DEAL_COLUMNS["created_date"]
        ),
    }


# ---------------------------------------------------------
# WORK ORDERS
# ---------------------------------------------------------

WORK_ORDER_COLUMNS = {
    "customer_code": "dropdown_mm6qz66s",
    "serial_number": "dropdown_mm6qawf5",
    "nature_of_work": "color_mm6qve7s",
    "last_executed_month": "color_mm6q7gm0",
    "execution_status": "color_mm6qpe77",

    "delivery_date": "date_mm6qybd",
    "po_date": "date_mm6qmqk3",

    "document_type": "color_mm6q7zpp",

    "start_date": "date_mm6qrzx2",
    "end_date": "date_mm6qbdxg",

    "owner": "color_mm6qthhv",
    "sector": "color_mm6qbz93",
    "work_type": "color_mm6qb2jp",

    "software_involvement": "color_mm6qxtw7",

    "last_invoice_date": "date_mm6q8yrg",
    "invoice_number": "dropdown_mm6qy338",

    "amount_excl_gst": "numeric_mm6qgnch",
    "amount_incl_gst": "numeric_mm6qnnfh",

    "billed_excl_gst": "numeric_mm6qznmn",
    "billed_incl_gst": "numeric_mm6qak8s",

    "collected_amount": "numeric_mm6qrpmr",

    "to_be_billed_excl_gst": "numeric_mm6qmgrb",
    "to_be_billed_incl_gst": "numeric_mm6q3y53",

    "receivable": "numeric_mm6qeeh5",

    "ar_priority": "color_mm6qvpbm",

    "quantity_ops": "numeric_mm6qewcv",
    "quantity_po": "dropdown_mm6qwn6h",
    "quantity_billed": "numeric_mm6q4mr3",
    "balance_quantity": "numeric_mm6qjnz1",

    "invoice_status": "color_mm6q756s",

    "expected_billing_month": "text_mm6qjw3b",
    "actual_billing_month": "color_mm6qce8s",
    "actual_collection_month": "text_mm6qrhn5",

    "wo_status": "color_mm6qetfs",

    "collection_status": "text_mm6qrz3f",
    "collection_date": "text_mm6qbtyg",

    "billing_status": "color_mm6qvsaa",
}


def normalize_work_order(item: dict) -> dict:

    columns = column_map(item)

    numeric_fields = {
        "amount_excl_gst",
        "amount_incl_gst",
        "billed_excl_gst",
        "billed_incl_gst",
        "collected_amount",
        "to_be_billed_excl_gst",
        "to_be_billed_incl_gst",
        "receivable",
        "quantity_ops",
        "quantity_billed",
        "balance_quantity",
    }

    result = {
        "id": item.get("id"),
        "name": clean_text(item.get("name")),
    }

    for field, column_id in WORK_ORDER_COLUMNS.items():

        value = columns.get(column_id)

        if field in numeric_fields:
            result[field] = clean_number(value)
        else:
            result[field] = clean_text(value)

    return result