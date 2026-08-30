def weighted_probability(probability: str | None) -> float:

    mapping = {
        "high": 0.75,
        "medium": 0.50,
        "low": 0.25,
    }

    if not probability:
        return 0.0

    return mapping.get(
        probability.strip().lower(),
        0.0
    )


def pipeline_summary(deals: list[dict]) -> dict:

    open_deals = [
        d for d in deals
        if (d.get("deal_status") or "").lower() == "open"
    ]

    total_pipeline = sum(
        d.get("deal_value") or 0
        for d in open_deals
    )

    weighted_pipeline = sum(
        (d.get("deal_value") or 0)
        * weighted_probability(d.get("probability"))
        for d in open_deals
    )

    return {
        "total_deals": len(deals),
        "open_deals": len(open_deals),
        "total_pipeline": round(total_pipeline, 2),
        "weighted_pipeline": round(weighted_pipeline, 2),
    }


def pipeline_by_sector(deals: list[dict]) -> list[dict]:

    result = {}

    for deal in deals:

        if (deal.get("deal_status") or "").lower() != "open":
            continue

        sector = deal.get("sector") or "Unknown"

        result[sector] = (
            result.get(sector, 0)
            + (deal.get("deal_value") or 0)
        )

    return [
        {
            "sector": sector,
            "pipeline": round(value, 2)
        }
        for sector, value in sorted(
            result.items(),
            key=lambda x: x[1],
            reverse=True
        )
    ]