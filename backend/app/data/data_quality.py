from collections import Counter


def check_deals(deals: list[dict]) -> dict:

    total = len(deals)

    missing_value = sum(
        1 for d in deals
        if d.get("deal_value") is None
    )

    missing_probability = sum(
        1 for d in deals
        if not d.get("probability")
    )

    missing_sector = sum(
        1 for d in deals
        if not d.get("sector")
    )

    return {
        "total_records": total,
        "missing_deal_value": missing_value,
        "missing_probability": missing_probability,
        "missing_sector": missing_sector,
    }


def check_work_orders(work_orders: list[dict]) -> dict:

    total = len(work_orders)

    missing_amount = sum(
        1 for w in work_orders
        if w.get("amount_incl_gst") is None
    )

    missing_billing = sum(
        1 for w in work_orders
        if w.get("billed_incl_gst") is None
    )

    missing_collection = sum(
        1 for w in work_orders
        if w.get("collected_amount") is None
    )

    missing_sector = sum(
        1 for w in work_orders
        if not w.get("sector")
    )

    return {
        "total_records": total,
        "missing_amount": missing_amount,
        "missing_billing": missing_billing,
        "missing_collection": missing_collection,
        "missing_sector": missing_sector,
    }