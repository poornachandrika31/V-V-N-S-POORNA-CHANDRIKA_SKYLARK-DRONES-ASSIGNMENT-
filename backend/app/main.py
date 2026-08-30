from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os

from app.monday.client import MondayClient
from app.data.normalizer import (
    normalize_deal,
    normalize_work_order
)
from app.analytics.service import BIService
from pydantic import BaseModel
from app.agent.agent import chat
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI(
    title="Skylark Business Intelligence Agent",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "application": "Skylark BI Agent",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


@app.get("/monday/test")
async def test_monday():

    deals_id = os.getenv("DEALS_BOARD_ID")
    work_orders_id = os.getenv("WORK_ORDERS_BOARD_ID")

    try:

        client = MondayClient()

        result = await client.get_boards([
            deals_id,
            work_orders_id
        ])

        return result

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )


@app.get("/monday/deals")
async def get_deals():

    board_id = os.getenv("DEALS_BOARD_ID")

    try:

        client = MondayClient()

        items = await client.get_board_items(board_id)

        return {
            "board": "deals",
            "count": len(items),
            "items": items
        }

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )


@app.get("/monday/work-orders")
async def get_work_orders():

    board_id = os.getenv("WORK_ORDERS_BOARD_ID")

    try:

        client = MondayClient()

        items = await client.get_board_items(board_id)

        return {
            "board": "work_orders",
            "count": len(items),
            "items": items
        }

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
@app.get("/monday/schema")
async def get_schema():

    deals_id = os.getenv("DEALS_BOARD_ID")
    work_orders_id = os.getenv("WORK_ORDERS_BOARD_ID")

    try:
        client = MondayClient()

        result = await client.get_boards_with_columns([
            deals_id,
            work_orders_id
        ])

        return result

    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
@app.get("/analytics/test")
async def analytics_test():

    deals_id = os.getenv("DEALS_BOARD_ID")
    work_orders_id = os.getenv("WORK_ORDERS_BOARD_ID")

    try:

        client = MondayClient()

        deal_items = await client.get_board_items(deals_id)

        work_order_items = await client.get_board_items(
            work_orders_id
        )

        deals = [
            normalize_deal(item)
            for item in deal_items
        ]

        work_orders = [
            normalize_work_order(item)
            for item in work_order_items
        ]

        return {
            "deals_count": len(deals),
            "work_orders_count": len(work_orders),

            "sample_deal": deals[0] if deals else None,

            "sample_work_order":
                work_orders[0]
                if work_orders
                else None
        }

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
@app.get("/analytics/dashboard")
async def analytics_dashboard():

    try:

        service = BIService()

        return await service.dashboard()

    except Exception as e:

        raise HTTPException(
            status_code=502,
            detail=str(e)
        )
class ChatRequest(BaseModel):
    message: str
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        result = await chat(request.message)
        return result

    except Exception as e:
        import traceback
        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )