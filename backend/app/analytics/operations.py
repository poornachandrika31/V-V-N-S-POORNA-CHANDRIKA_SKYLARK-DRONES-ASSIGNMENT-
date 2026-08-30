def execution_summary(work_orders: list[dict]) -> dict:

    result = {}

    for wo in work_orders:

        status = wo.get("execution_status") or "Unknown"

        result[status] = result.get(status, 0) + 1

    return result


def sector_summary(work_orders: list[dict]) -> dict:

    result = {}

    for wo in work_orders:

        sector = wo.get("sector") or "Unknown"

        result[sector] = result.get(sector, 0) + 1

    return result