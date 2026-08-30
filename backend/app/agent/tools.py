from app.analytics.service import BIService


async def get_pipeline_summary():
    """Get the current open sales pipeline and weighted pipeline."""

    service = BIService()
    deals, _ = await service.load_data()

    from app.analytics.pipeline import pipeline_summary

    return pipeline_summary(deals)


async def get_pipeline_by_sector():
    """Get open pipeline broken down by sector."""

    service = BIService()
    deals, _ = await service.load_data()

    from app.analytics.pipeline import pipeline_by_sector

    return pipeline_by_sector(deals)


async def get_financial_summary():
    """Get order value, billing, collection and receivables."""

    service = BIService()
    _, work_orders = await service.load_data()

    from app.analytics.finance import finance_summary

    return finance_summary(work_orders)


async def get_receivables():
    """Get receivables grouped by AR priority."""

    service = BIService()
    _, work_orders = await service.load_data()

    from app.analytics.finance import receivable_by_priority

    return receivable_by_priority(work_orders)


async def get_deal_risks():
    """Identify potentially risky open deals."""

    service = BIService()
    deals, _ = await service.load_data()

    from app.analytics.risk import deal_risks

    return deal_risks(deals)[:20]


async def get_data_quality():
    """Report missing and incomplete business data."""

    service = BIService()
    deals, work_orders = await service.load_data()

    from app.data.data_quality import (
        check_deals,
        check_work_orders,
    )

    return {
        "deals": check_deals(deals),
        "work_orders": check_work_orders(work_orders),
    }