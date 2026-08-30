from datetime import date


def deal_risks(deals: list[dict]) -> list[dict]:

    risks = []

    for deal in deals:

        if (deal.get("deal_status") or "").lower() != "open":
            continue

        risk_reasons = []

        probability = (
            deal.get("probability") or ""
        ).lower()

        stage = (
            deal.get("deal_stage") or ""
        ).lower()

        # Low-probability open deal
        if probability == "low":
            risk_reasons.append(
                "Low closure probability"
            )

        # Missing close date
        if not deal.get("close_date"):
            risk_reasons.append(
                "Close date is missing"
            )

        # Missing tentative close date
        if not deal.get("tentative_close_date"):
            risk_reasons.append(
                "Tentative close date is missing"
            )

        # Deal stuck in early stage
        if "lead" in stage:
            risk_reasons.append(
                "Deal is still in an early sales stage"
            )

        if risk_reasons:

            risks.append({
                "deal_id": deal.get("id"),
                "deal_name": deal.get("name"),
                "deal_value": deal.get("deal_value"),
                "sector": deal.get("sector"),
                "probability": deal.get("probability"),
                "risk_reasons": risk_reasons,
                "risk_count": len(risk_reasons),
            })

    return sorted(
        risks,
        key=lambda x: (
            x["risk_count"],
            x["deal_value"] or 0
        ),
        reverse=True
    )