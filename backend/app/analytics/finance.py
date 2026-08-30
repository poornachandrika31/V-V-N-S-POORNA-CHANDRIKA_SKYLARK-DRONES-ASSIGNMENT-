def finance_summary(work_orders: list[dict]) -> dict:

    total_amount = sum(
        w.get("amount_incl_gst") or 0
        for w in work_orders
    )

    billed = sum(
        w.get("billed_incl_gst") or 0
        for w in work_orders
    )

    collected = sum(
        w.get("collected_amount") or 0
        for w in work_orders
    )

    receivable = sum(
        w.get("receivable") or 0
        for w in work_orders
    )

    to_be_billed = sum(
        w.get("to_be_billed_incl_gst") or 0
        for w in work_orders
    )

    collection_rate = (
        collected / billed * 100
        if billed > 0
        else 0
    )

    billing_rate = (
        billed / total_amount * 100
        if total_amount > 0
        else 0
    )

    return {
        "total_order_value": round(total_amount, 2),
        "total_billed": round(billed, 2),
        "total_collected": round(collected, 2),
        "total_receivable": round(receivable, 2),
        "total_to_be_billed": round(to_be_billed, 2),
        "billing_rate_pct": round(billing_rate, 2),
        "collection_rate_pct": round(collection_rate, 2),
    }


def receivable_by_priority(
    work_orders: list[dict]
) -> list[dict]:

    result = {}

    for wo in work_orders:

        priority = wo.get("ar_priority") or "Unknown"

        amount = wo.get("receivable") or 0

        result[priority] = (
            result.get(priority, 0) + amount
        )

    return [
        {
            "priority": priority,
            "receivable": round(amount, 2)
        }
        for priority, amount in sorted(
            result.items(),
            key=lambda x: x[1],
            reverse=True
        )
    ]