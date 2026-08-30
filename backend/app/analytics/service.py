import os

from app.monday.client import MondayClient

from app.data.normalizer import (
    normalize_deal,
    normalize_work_order,
)

from app.data.data_quality import (
    check_deals,
    check_work_orders,
)

from app.analytics.pipeline import (
    pipeline_summary,
    pipeline_by_sector,
)

from app.analytics.finance import (
    finance_summary,
    receivable_by_priority,
)

from app.analytics.risk import (
    deal_risks,
)


class BIService:

    async def load_data(self):

        client = MondayClient()

        deals_raw = await client.get_board_items(
            os.getenv("DEALS_BOARD_ID")
        )

        work_orders_raw = await client.get_board_items(
            os.getenv("WORK_ORDERS_BOARD_ID")
        )

        deals = [
            normalize_deal(x)
            for x in deals_raw
        ]

        work_orders = [
            normalize_work_order(x)
            for x in work_orders_raw
        ]

        return deals, work_orders


    async def dashboard(self):

        deals, work_orders = await self.load_data()

        return {

            "pipeline":
                pipeline_summary(deals),

            "pipeline_by_sector":
                pipeline_by_sector(deals),

            "finance":
                finance_summary(work_orders),

            "receivables":
                receivable_by_priority(work_orders),

            "risks":
                deal_risks(deals)[:20],

            "data_quality": {

                "deals":
                    check_deals(deals),

                "work_orders":
                    check_work_orders(work_orders),
            }
        }